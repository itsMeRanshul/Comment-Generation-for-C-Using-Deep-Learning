import tempfile
import os
import shutil
import re
from pycparser import c_parser, c_ast, parse_file

def extract_code_blocks(code: str):
    """
    Extracts more semantically meaningful blocks of code from the input C code
    for better commenting. This is a heuristic approach.
    """
    try:
        lines = code.split('\n')
        blocks = []
        current_block = []
        brace_level = 0
        
        for i, line in enumerate(lines):
            stripped_line = line.strip()
            
            # Skip empty lines and single-line comments for block detection
            if not stripped_line or stripped_line.startswith('//'):
                if current_block: # If there's a pending block, add it before skipping
                    blocks.append('\n'.join(current_block).strip())
                    current_block = []
                continue

            current_block.append(line)

            # Check for brace changes to define blocks
            open_braces = line.count('{')
            close_braces = line.count('}')
            
            brace_level += open_braces
            brace_level -= close_braces

            # Heuristic for block termination:
            # - If we are at brace_level 0 (outside any block), and the current line
            #   contains a closing brace, or is a standalone statement (ends with ';')
            #   and not part of a multi-line construct (like a function signature without opening brace)
            # - Or if a significant construct (like a function definition or loop start) is encountered
            
            # Simple heuristic for function definitions, loops, if statements
            is_function_start = re.match(r'^(void|int|char|float|double|long|short)\s+\w+\s*\(.*\)\s*\{', stripped_line)
            is_control_flow_start = re.match(r'^(for|while|do|if|else if|else)\s*\(.*\)\s*\{?', stripped_line)
            is_standalone_statement = stripped_line.endswith(';') and not stripped_line.startswith('#')

            if is_function_start or is_control_flow_start:
                if current_block and len(current_block) > 1: # Avoid re-adding the current line if it's new block start
                    blocks.append('\n'.join(current_block[:-1]).strip())
                    current_block = [line] # Start a new block with this line
                # If brace level becomes 0 after processing, and it's a function/control flow start, it likely ends a previous block.
                # Or if the line itself completes a block (e.g., `int x = 0;`)
            elif brace_level == 0 and (close_braces > 0 or is_standalone_statement):
                blocks.append('\n'.join(current_block).strip())
                current_block = []
            elif brace_level < 0: # Error condition, too many closing braces
                print(f"Warning: Mismatched braces detected near line {i+1}. Resetting brace level.")
                blocks.append('\n'.join(current_block).strip())
                current_block = []
                brace_level = 0 # Reset for next attempt
            
        # Add any remaining block
        if current_block:
            blocks.append('\n'.join(current_block).strip())
            
        # Filter out empty blocks
        return [block for block in blocks if block]
    except Exception as e:
        raise ValueError(f"Error extracting code blocks: {str(e)}")

MANUAL_FAKE_LIBC_INCLUDE_PATH = "C:/Users/RANSHUL/AppData/Local/Programs/Python/Python38/Lib/site-packages/pycparser/utils/fake_libc_include"


import os
import tempfile
from pycparser import parse_file, c_ast

MANUAL_FAKE_LIBC_INCLUDE_PATH = "C:/Users/RANSHUL/AppData/Local/Programs/Python/Python38/Lib/site-packages/pycparser/utils/fake_libc_include"

def extract_linear_ast(code: str) -> str:
    """Generates a linearized AST from C code using pycparser."""
    tmp_path = None
    try:
        # Create a temporary file with the C code
        with tempfile.NamedTemporaryFile(suffix=".c", delete=False, mode='w', encoding='utf-8') as tmp:
            tmp.write(code)
            tmp_path = tmp.name

        # Determine the fake libc include path
        fake_libc_path = MANUAL_FAKE_LIBC_INCLUDE_PATH if os.path.isdir(MANUAL_FAKE_LIBC_INCLUDE_PATH) else None
        if not fake_libc_path:
            raise FileNotFoundError("fake_libc_include directory not found.")

        # Parse the file to generate the AST
        ast = parse_file(tmp_path, use_cpp=True, cpp_args=[f'-I{fake_libc_path}'])

        # Custom AST linearizer
        class ASTLinearizer(c_ast.NodeVisitor):
            def __init__(self):
                self.nodes = []

            def visit_FileAST(self, node):
                self.nodes.append("FileAST")
                self.generic_visit(node)

            def visit_FuncDef(self, node):
                self.nodes.append("FuncDef")
                self.generic_visit(node)

            def visit_FuncCall(self, node):
                self.nodes.append("FuncCall")
                self.generic_visit(node)

            def visit_Return(self, node):
                self.nodes.append("Return")
                self.generic_visit(node)

        # Linearize the AST
        linearizer = ASTLinearizer()
        linearizer.visit(ast)

        return " ".join(linearizer.nodes)
    except Exception as e:
        return f"Error: {e}"
    finally:
        # Clean up the temporary file
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)
