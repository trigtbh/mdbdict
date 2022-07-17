# MDBDict
MDBDict allows you to access MongoDB databases through an automatically updating dictionary

## Installation
To install, run the following command:
```
pip install mdbdict
```

Alternatively, you can download the source code and install it yourself:
```
git clone https://github.com/trigtbh/mdbdict.git
cd mdbdict
pip install -r requirements.txt
python setup.py install
```
---
## Usage

### Opening a cluster
```python
import mdbdict as md
db = md.MDict('mongodb://localhost:27017/') # Replace with your MongoDB URI
```
The contents of the cluster specified by your URI will be loaded into the dictionary.

---
### Displaying the contents of a collection
```python
collection = db['database']['collection'] # Collections are treated as lists of dictionaries
# The first key is the name of the database
# The second key is the name of the specific collection within the database
print(collection)
```
---
### Adding a document to a collection

```python
collection.append({"_id": 1, "name": "John Doe"})
```
---
### Editing a document in a collection

```python
document = collection[0]
document["name"] = "Jane Doe" # This change will be automatically saved to MongoDB
```
---
### Deleting a document in a collection

```python
del collection[0]
```