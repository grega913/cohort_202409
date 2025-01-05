import pickle
from icecream import ic
import os
import sys




data_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(data_dir, "data", "attention.pdf")
output_path = os.path.join(data_dir,"output")
persistence_directory = os.path.join(data_dir, "vectorstore")

pkl_file_path = os.path.join(data_dir, "pkl1.pkl")

ic(data_dir)
ic(file_path)
ic(output_path)
ic(persistence_directory)


# Create a Python object
my_object = {"name": "John", "age": 35}


# Open a file in binary write mode
with open(pkl_file_path, "wb") as f:
    # Use pickle to serialize the object and write it to the file
    pickle.dump(my_object, f, protocol=pickle.HIGHEST_PROTOCOL)

# Now, let's read the object back from the file
with open(pkl_file_path, "rb") as f:
    # Use pickle to deserialize the object from the file
    loaded_object = pickle.load(f)



# Open a file in binary write mode
with open("my_object.pkl", "wb") as f:
    # Use pickle to serialize the object and write it to the file
    pickle.dump(my_object, f, protocol=pickle.HIGHEST_PROTOCOL)

# Now, let's read the object back from the file
with open("my_object.pkl", "rb") as f:
    # Use pickle to deserialize the object from the file
    loaded_object = pickle.load(f)

print(loaded_object)  # Output: {'name': 'John', 'age': 30}