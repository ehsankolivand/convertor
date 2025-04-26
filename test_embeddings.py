"""
Test script for the embedding generator.
"""

from pdf2vector.core.embeddings import EmbeddingGenerator
import numpy as np

def test_embeddings():
    # Initialize the embedding generator
    generator = EmbeddingGenerator()
    
    # Test single text embedding
    text = "This is a test sentence."
    embedding = generator.embed_text(text)
    
    # Verify embedding properties
    print(f"\nSingle text embedding test:")
    print(f"Input text: {text}")
    print(f"Embedding dimension: {len(embedding)}")
    print(f"Embedding norm: {np.linalg.norm(embedding)}")
    
    # Test multiple texts embedding
    texts = ["First sentence.", "Second sentence.", "Third sentence."]
    embeddings = generator.embed_text(texts)
    
    # Verify multiple embeddings
    print(f"\nMultiple texts embedding test:")
    print(f"Number of embeddings: {len(embeddings)}")
    print(f"All embeddings have correct dimension: {all(len(e) == 1536 for e in embeddings)}")
    print(f"All embeddings are normalized: {all(abs(np.linalg.norm(e) - 1.0) < 1e-6 for e in embeddings)}")
    
    # Test similarity between different texts
    print(f"\nSimilarity test:")
    sim1 = np.dot(embeddings[0], embeddings[1])
    sim2 = np.dot(embeddings[0], embeddings[2])
    print(f"Similarity between first and second text: {sim1:.4f}")
    print(f"Similarity between first and third text: {sim2:.4f}")

if __name__ == "__main__":
    test_embeddings() 