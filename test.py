from main import process_message

msg = "¿Dónde puedo encontrar un banco de comida cerca de mí?"
result = process_message(msg)

print(result)

'''
print("\nTop matching nonprofits:")
for score, idx in zip(top_results[0], top_results[1]):
    idx = int(idx)  # Convert tensor to integer
    print(f"\nScore: {score:.4f}")
    print(f"Name: {df.iloc[idx]['Name']}")
    print(f"URL: {df.iloc[idx]['URL']}")
    print(f"Category: {df.iloc[idx]['Category']}")
    print(f"Summary: {df.iloc[idx]['Summary'][:300]}...")



query = input("Enter Query: ")
query_embedding = model.encode(query, convert_to_tensor=True)

cos_scores = util.cos_sim(query_embedding, summary_embeddings)[0]

top_k = 5
top_results = cos_scores.topk(k=top_k)

print("\nTop matching nonprofits:")
for score, idx in zip(top_results[0], top_results[1]):
    idx = int(idx)  # Convert tensor to integer
    print(f"\nScore: {score:.4f}")
    print(f"Name: {df.iloc[idx]['Name']}")
    print(f"URL: {df.iloc[idx]['URL']}")
    print(f"Category: {df.iloc[idx]['Category']}")
    print(f"Summary: {df.iloc[idx]['Summary'][:300]}...")
'''