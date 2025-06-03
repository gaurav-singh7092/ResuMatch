#!/usr/bin/env python3
"""
This script monkeypatches the SentenceTransformer library to work around the cached_download issue.
Run this during the build process on Render.
"""
import os
import sys
import importlib.util
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def find_module_path(module_name):
    """Find the path of a module"""
    try:
        spec = importlib.util.find_spec(module_name)
        if spec and spec.origin:
            return spec.origin
    except (ImportError, AttributeError):
        pass
    return None

def patch_sentence_transformers():
    """Patch the sentence_transformers library to handle missing cached_download"""
    try:
        # Find the SentenceTransformer.py file
        st_file = find_module_path("sentence_transformers.SentenceTransformer")
        if not st_file or not os.path.exists(st_file):
            logger.error("Could not find SentenceTransformer.py file")
            return False
        
        # Read the file
        with open(st_file, 'r') as f:
            content = f.read()
        
        # Check if it uses cached_download
        if "cached_download" in content:
            logger.info("Found cached_download in SentenceTransformer.py")
            
            # Create a patch that replaces cached_download with hf_hub_download
            patched_content = content.replace(
                "from huggingface_hub import HfApi, HfFolder, Repository, hf_hub_url, cached_download",
                "from huggingface_hub import HfApi, HfFolder, Repository, hf_hub_url\n" +
                "# Patched by fix_huggingface.py\n" +
                "try:\n" +
                "    from huggingface_hub import cached_download\n" +
                "except ImportError:\n" +
                "    from huggingface_hub import hf_hub_download as cached_download"
            )
            
            # Write the patched content
            with open(st_file, 'w') as f:
                f.write(patched_content)
            
            logger.info("Successfully patched SentenceTransformer.py")
            return True
        else:
            logger.info("SentenceTransformer.py does not use cached_download, no patch needed")
            return True
    except Exception as e:
        logger.error(f"Error patching sentence_transformers: {str(e)}")
        return False

if __name__ == "__main__":
    print("Checking for huggingface_hub compatibility issues...")
    success = patch_sentence_transformers()
    sys.exit(0 if success else 1)
