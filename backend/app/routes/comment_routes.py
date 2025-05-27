from fastapi import APIRouter, HTTPException, Depends
from app.schemas.request_schema import CodeRequest, CommentResponse, CodeBlockComment
from app.utils.ast_parser import extract_code_blocks, extract_linear_ast
from app.models.model import CodeCommentModel

# Create an APIRouter instance
router = APIRouter()

# --- Dependency for the model ---
# This ensures the model is loaded only once when the application starts
# and is reused for all requests.
def get_comment_model():
    # This will load the model the first time it's requested
    # and then reuse the same instance.
    return CodeCommentModel()

@router.get("/")
def root():
    """
    Root endpoint for the API.
    """
    return {"message": "Connected from routes!"}

@router.post("/generate", response_model=CommentResponse)
def generate_comment(
    data: CodeRequest,
    model_instance: CodeCommentModel = Depends(get_comment_model) # Inject the model instance
):
    """
    Generates comments and linearized AST for the provided code.
    """
    try:
        code = data.code
        
        # Extract the linearized AST
        ast_linear = extract_linear_ast(code)
        
        # Extract code blocks for commenting
        blocks = extract_code_blocks(code)
        comments = []
        
        for block in blocks:
            # Use the injected model instance
            comment = model_instance.predict_comment(block)
            comments.append({"block": block, "comment": comment})
        
        # Return the AST and block-wise comments
        return CommentResponse(ast_linear=ast_linear, comments=comments)
    except ValueError as ve: # Catch specific errors from your utility functions
        raise HTTPException(status_code=400, detail=f"Code processing error: {str(ve)}")
    except Exception as e:
        # Log the full exception for debugging in production
        import traceback
        traceback.print_exc() 
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")