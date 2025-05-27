from transformers import RobertaTokenizer, T5ForConditionalGeneration
import torch

class CodeCommentModel:
    def __init__(self, model_dir="C:/Users/RANSHUL/OneDrive/Desktop/compiler/codet5-comment-gen-final"):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # Load Roberta tokenizer and T5 model
        self.tokenizer = RobertaTokenizer.from_pretrained(model_dir)
        self.model = T5ForConditionalGeneration.from_pretrained(model_dir)
        self.model.to(self.device)
        self.model.eval()

    def predict_comment(self, code_block: str) -> str:
        """
        Predicts a comment for a given code block.
        Includes prompt engineering and adjusted generation parameters.
        """
        # Add a prompt to guide the model
        # Experiment with different prompts:
        # prompt = f"Generate a concise and accurate comment for the following C code block:\n{code_block}"
        prompt = f"Comment this C code:\n{code_block}"
        # prompt = f"Explain the purpose of the following C code:\n{code_block}"


        # Tokenize the input string
        inputs = self.tokenizer(
            prompt, # Use the prompted input
            return_tensors="pt",
            truncation=True,
            max_length=512,
            padding=True
        ).to(self.device)

        # Generate predictions
        with torch.no_grad():
            outputs = self.model.generate(
                inputs["input_ids"],
                max_length=50, # Reduced max_length for conciseness. Adjust as needed.
                num_beams=5,  # Slightly increased num_beams for more diverse search
                early_stopping=True,
                no_repeat_ngram_size=2, # Prevent repeating n-grams (e.g., "Base case // Base case")
                temperature=0.7, # Introduce a bit of randomness to avoid exact repetitions (try 0.7-1.0)
                top_k=50, # Consider top_k samples for diversity
                top_p=0.95 # Nucleus sampling for diversity
            )

        return self.tokenizer.decode(outputs[0], skip_special_tokens=True).strip()