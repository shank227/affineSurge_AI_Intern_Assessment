from app.versioning import compare_versions

result = compare_versions("v1", "v2")

print("Changed:")
for item in result["changed"]:
    print(item)

print("\nNew:")
for item in result["new"]:
    print(item)

print("\nRemoved:")
for item in result["removed"]:
    print(item)