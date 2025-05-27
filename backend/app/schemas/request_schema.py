from pydantic import BaseModel
from typing import List

class CodeRequest(BaseModel):
    code: str

class CodeBlockComment(BaseModel):
    block: str
    comment: str

class CommentResponse(BaseModel):
    ast_linear: str
    comments: List[CodeBlockComment]
