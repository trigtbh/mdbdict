# MDBDict
MDBDict allows you to access MongoDB databases through an automatically updating dictionary

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