"""
Adapted from https://github.com/garg-aayush/building-from-scratch/blob/main/transformers/gpt-2/fineweb-modal.py

FineWeb-Edu Dataset Tokenization with Modal

This script demonstrates how to use Modal's distributed computing platform to efficiently 
download and tokenize the FineWeb-Edu dataset from HuggingFace.

What this script does:
1. Downloads parquet files from the FineWeb-Edu dataset in parallel
2. Tokenizes the text data using GPT-2's tiktoken encoder
3. Creates training shards suitable for language model training
4. Stores everything in Modal's persistent volumes

Prerequisites:
- Modal account (sign up at modal.com)
- Modal CLI installed: pip install modal
- Authentication: modal setup

Usage:
    modal run fineweb-modal.py

The script will process the FineWeb-Edu 10BT sample, downloading and tokenizing
all parquet files in parallel, then creating training shards of 100M tokens each.
"""

import modal

# =============================================================================
# MODAL SETUP AND CONFIGURATION
# =============================================================================
# Create a Modal App - this is the container for all your functions and resources
# Think of it as your "project" in Modal's cloud environment
app = modal.App("fineweb-edu-tokenizer")

# Define a custom container image with all required dependencies
# Modal will build this image once and reuse it for all function calls
# This ensures consistent environments and faster cold starts
image = modal.Image.debian_slim(python_version="3.11").pip_install(
    "datasets",
    "tiktoken",
    "numpy",
    "tqdm",
    "huggingface_hub",
    "pandas",
    "pyarrow",
    "requests"
)

# Create a persistent volume for storing downloaded data and tokens
# Volumes persist across function calls and can be shared between functions
volume = modal.Volume.from_name("fineweb-edu-10BT-data", create_if_missing=True)

# =============================================================================
# CONFIGURATION PARAMETERS
# =============================================================================

# Dataset configuration
REMOTE_NAME = "10BT"              # Which split of FineWeb-Edu to use (10BT = 10 billion tokens)
SHARD_SIZE = int(1e8)            # 100M tokens per training shard (standard for LLM training)
REPO_ID = "HuggingFaceFW/fineweb-edu"  # HuggingFace dataset repository


# =============================================================================
# MODAL FUNCTIONS - The core distributed processing functions
# =============================================================================

@app.function(
    image=image,                          # Use our custom container image
    volumes={"/data": volume},            # Mount persistent storage at /data
    timeout=600,                          # Allow up to 10 minutes for execution
    retries=3,                            # Retry failed calls automatically
)
def process_dataset():
    """
    Main orchestration function that discovers parquet files and launches parallel processing.
    """
    from huggingface_hub import HfApi
    
    print("Discovering parquet files in FineWeb-Edu dataset...")
    
    # Initialize HuggingFace API client
    api = HfApi()
    
    # List all files in the dataset repository
    files = api.list_repo_files(REPO_ID, repo_type="dataset")
    # Filter for parquet files in the sample-10BT split
    parquet_files = [f for f in files if f.startswith(f"sample/{REMOTE_NAME}/") and f.endswith(".parquet")]
    # sort parquet_files by filename
    parquet_files.sort()
    print(f"Found {len(parquet_files)} parquet files to download")
    # Create direct download URLs
    base_url = f"https://huggingface.co/datasets/{REPO_ID}/resolve/main/"
    parquet_urls = [base_url + f for f in parquet_files]
    results = list(download_and_tokenize_file.map(parquet_urls))
    create_training_shards.remote()
    return results


@app.function(
    image=image,
    volumes={"/data": volume},
    timeout=600,
    cpu=4,
    memory=1024 * 16,
    retries=3,
)
def download_and_tokenize_file(parquet_url: str) -> dict:
    """
    Download a single parquet file and tokenize its contents.
    """
    import os
    import time

    import numpy as np
    import pandas as pd
    import requests
    import tiktoken
    
    start_time = time.time()
    
    # Extract filename from URL for local storage
    filename = parquet_url.split("/")[-1]
    parquet_path = f"/data/parquet/{filename}"
    tokens_path = f"/data/tokens/{filename.replace('.parquet', '.npy')}"
    
    # Create directories if they don't exist
    # Modal volumes persist across function calls, so this is safe
    os.makedirs(os.path.dirname(parquet_path), exist_ok=True)
    os.makedirs(os.path.dirname(tokens_path), exist_ok=True)

    print(f"Processing {filename}...")
    
    # =================================================================
    # STEP 1: Download the parquet file
    # =================================================================
    if os.path.exists(parquet_path):
        print(f"Parquet file already exists: {filename}")
        file_size_mb = os.path.getsize(parquet_path) / (1024 * 1024)
        print(f"File size: {file_size_mb:.2f} MB")
    else:
        print(f"Downloading {filename}...")
        
        # Use streaming download for large files to avoid memory issues
        response = requests.get(parquet_url, stream=True, timeout=300)
        response.raise_for_status()
        
        # Save to persistent volume
        with open(parquet_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        file_size_mb = os.path.getsize(parquet_path) / (1024 * 1024)
        print(f"Downloaded {filename} ({file_size_mb:.2f} MB)")
        

    # =================================================================
    # STEP 2: Tokenize the text data
    # =================================================================
    if os.path.exists(tokens_path):
        print(f"Tokens already exist: {filename}")
        tokens_np = np.load(tokens_path)
        num_tokens = len(tokens_np)
    else:
        print(f"Tokenizing {filename}...")
        # Load the parquet file into memory
        df = pd.read_parquet(parquet_path)
        print(f"Loaded {len(df)} documents from {filename}")
        
        # Initialize GPT-2 tokenizer (same as used by OpenAI's models)
        enc = tiktoken.get_encoding("gpt2")
        eot_token = enc._special_tokens["<|endoftext|>"]  # End-of-text delimiter
        
        # Tokenize all documents in the file
        all_tokens = []
        for i, text in enumerate(df['text']):
            # Add end-of-text token as document separator (standard practice)
            doc_tokens = [eot_token] + enc.encode_ordinary(text)
            all_tokens.extend(doc_tokens)
            
            # Progress reporting for large files
            if (i + 1) % 10000 == 0:
                print(f"  Tokenized {i + 1}/{len(df)} documents...")
        
        # Convert to numpy array with efficient uint16 storage
        # GPT-2 vocabulary is 50,257 tokens, which fits in uint16 (0-65,535)
        tokens_np = np.array(all_tokens, dtype=np.uint16)
        num_tokens = len(tokens_np)
        
        # Validate token range for uint16 storage
        assert (tokens_np >= 0).all() and (tokens_np < 2**16).all(), "Token values exceed uint16 range!"
        
        # Save tokenized data to persistent volume
        np.save(tokens_path, tokens_np)
        print(f"Saved {num_tokens:,} tokens to {tokens_path}")

    
    # Commit changes to the volume to ensure persistence
    volume.commit()
    
    return {
        "filename": filename,
        "parquet_url": parquet_url,
        "parquet_path": parquet_path,
        "tokens_path": tokens_path,
        "num_tokens": num_tokens,
        "file_size_mb": file_size_mb
    }

@app.function(
    image=image,
    volumes={"/data": volume},
    timeout=600,
    cpu=4,
    memory=1024 * 16,
    retries=3,
)
def create_training_shards():
    """
    Combine all tokenized files into fixed-size training shards of 100M tokens. 
    """
    import os

    import numpy as np
    
    print("Creating training shards from tokenized files...")
    
    # Directory setup
    tokens_dir = "/data/tokens"
    shards_dir = "/data/shards"
    os.makedirs(shards_dir, exist_ok=True)
    
    # Find all tokenized files
    token_files = [f for f in os.listdir(tokens_dir) if f.endswith(".npy")]
    token_files.sort()  # Process in consistent order
    
    if not token_files:
        print("No tokenized files found! Run tokenization first.")
        return
    print(f"Found {len(token_files)} tokenized files to process")
    
    # Initialize shard creation state
    remaining_tokens = None  # Tokens left over from previous file
    shard_index = 0          # Current shard number
    total_tokens_processed = 0
    
    # Process each tokenized file
    for file_idx, token_file in enumerate(token_files):
        file_path = f"{tokens_dir}/{token_file}"
        print(f"Processing {token_file} ({file_idx + 1}/{len(token_files)})...")
        
        # Load tokenized data
        current_tokens = np.load(file_path)
        print(f"Loaded {len(current_tokens):,} tokens")
        
        # Combine with any leftover tokens from previous files
        if remaining_tokens is not None:
            print(f"Combining with {len(remaining_tokens):,} remaining tokens")
            current_tokens = np.concatenate([remaining_tokens, current_tokens])
        
        total_file_tokens = len(current_tokens)
        print(f"Total tokens available: {total_file_tokens:,}")
        
        # Create as many complete shards as possible
        num_complete_shards = total_file_tokens // SHARD_SIZE
        print(f"Can create {num_complete_shards} complete shards")
        
        for shard_idx in range(num_complete_shards):
            # Determine split: first shard is validation, rest are training
            # This is a common practice in LLM training
            split = "val" if shard_index == 0 else "train"
            
            # Extract shard tokens
            start_idx = shard_idx * SHARD_SIZE
            end_idx = (shard_idx + 1) * SHARD_SIZE
            shard_tokens = current_tokens[start_idx:end_idx]
            
            # Save shard with descriptive filename
            shard_filename = f"finewebedu_{REMOTE_NAME}_{split}_{shard_index:04d}.npy"
            shard_path = f"{shards_dir}/{shard_filename}"
            
            np.save(shard_path, shard_tokens)
            print(f"Saved shard {shard_index}: {shard_filename} ({len(shard_tokens):,} tokens)")
            
            shard_index += 1
            total_tokens_processed += len(shard_tokens)
        
        # Save remaining tokens for next iteration
        remaining_start_idx = num_complete_shards * SHARD_SIZE
        remaining_tokens = current_tokens[remaining_start_idx:]
        
        if len(remaining_tokens) > 0:
            print(f"{len(remaining_tokens):,} tokens remaining for next shard")
        else:
            remaining_tokens = None
    
    # Handle any final remaining tokens
    if remaining_tokens is not None and len(remaining_tokens) > 0:
        # Save final partial shard (this is normal for the last shard)
        split = "train"  # Partial shards go to training set
        final_filename = f"finewebedu_{REMOTE_NAME}_{split}_{shard_index:04d}.npy"
        final_path = f"{shards_dir}/{final_filename}"
        
        np.save(final_path, remaining_tokens)
        print(f"Saved final partial shard: {final_filename} ({len(remaining_tokens):,} tokens)")
        total_tokens_processed += len(remaining_tokens)
        shard_index += 1
    
    # Commit all changes to persistent storage
    volume.commit()
    
    # List created shards
    shard_files = sorted([f for f in os.listdir(shards_dir) if f.endswith('.npy')])
    val_shards = [f for f in shard_files if '_val_' in f]
    train_shards = [f for f in shard_files if '_train_' in f]
    
    return {
        "total_shards": shard_index,
        "total_tokens": total_tokens_processed,
        "validation_shards": len(val_shards),
        "training_shards": len(train_shards)
    }


# =============================================================================
# MAIN ENTRY POINT - This runs when you call `modal run`
# =============================================================================
@app.local_entrypoint()
def main():
    """
    Main entry point for the FineWeb-Edu tokenization pipeline.
    """
    print("Starting FineWeb-Edu Dataset Tokenization Pipeline")
    process_dataset.remote()