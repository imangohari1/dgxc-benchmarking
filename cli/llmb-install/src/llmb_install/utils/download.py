# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: MIT
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.


"""Shared download helpers for LLMB installer."""

import urllib.error
import urllib.request
from pathlib import Path


def download_file(url: str, dest_path: str | Path) -> None:
    """Download a file from URL to a destination path with progress indication.

    Args:
        url: URL to download from
        dest_path: Local path to save file to

    Raises:
        RuntimeError: If the download fails for any reason.
    """
    try:

        def _progress_hook(block_num, block_size, total_size):
            """Simple progress indicator."""
            if total_size > 0:
                percent = min(100, (block_num * block_size * 100) // total_size)
                if block_num % 50 == 0:  # Update every 50 blocks to avoid spam
                    print(f"  Progress: {percent}%", end='\r', flush=True)

        urllib.request.urlretrieve(url, dest_path, reporthook=_progress_hook)
        print("  Progress: 100%")  # Final progress update

    except urllib.error.HTTPError as e:
        raise RuntimeError(f"Failed to download from {url}: HTTP {e.code} - {e.reason}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"Failed to download from {url}: {e.reason}") from e
    except Exception as e:
        raise RuntimeError(f"Failed to download from {url}: {str(e)}") from e
