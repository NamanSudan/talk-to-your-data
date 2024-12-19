
from vanna.remote import VannaDefault

# Initialize with your credentials
api_key = 'ec06a61c6fde4d6a9fb0208f51f6a222'  # Using the same API key from your vanna_wrapper.py
model_name = 'thepunisher'  # Using the same model from your vanna_wrapper.py

# Initialize Vanna with new method
vn = VannaDefault(model=model_name, api_key=api_key)

# Print current model (using the correct attribute name)
print("Current model:", vn._model)
