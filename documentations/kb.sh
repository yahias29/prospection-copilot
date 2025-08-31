#!/usr/bin/env bash

# A simple, reliable script to build the knowledge base for a custom GPT.

# --- Configuration ---
# The file that lists which source files to include.
SPEC_FILE="kb.txt"
# The final output file for the GPT to read.
OUTPUT_FILE="kb.md"
# --- End of Configuration ---

# Exit immediately if a command fails.
set -e

echo "✅ 1- Generating Knowledge Base..."

# Check if the specification file exists.
if [ ! -f "$SPEC_FILE" ]; then
    echo "❌ Error: Specification file not found at '$SPEC_FILE'"
    exit 1
fi

echo "→ Cleaning previous file..."
# Create an empty output file, overwriting any old one.
> "$OUTPUT_FILE"

echo "→ Building knowledge base from '$SPEC_FILE'..."

# Read each line from kb.txt
while IFS= read -r file_path || [[ -n "$file_path" ]]; do
    # Skip empty lines
    if [ -z "$file_path" ]; then
        continue
    fi
    
    # Go back to the project's root directory to find the file
    file_to_include="../$file_path"
    
    if [ -f "$file_to_include" ]; then
        echo "  - Adding content from: $file_path"
        # Append a header with the file path
        echo "---" >> "$OUTPUT_FILE"
        echo "File: \`$file_path\`" >> "$OUTPUT_FILE"
        echo "---" >> "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE"
        # Append the file's content
        cat "$file_to_include" >> "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE" # Add a newline for spacing
    else
        echo "  ⚠️ Warning: Could not find file '$file_path', skipping."
    fi
done < "$SPEC_FILE"

echo "✅ 2- Knowledge base generation complete!"
echo "➡️  Output file is ready at: '$OUTPUT_FILE'"