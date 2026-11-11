# Personal AI translator experiment

`StoryForge-Translator-Personal-AI-20.ipynb` is an isolated experimental notebook.
The current production notebook and manifest remain unchanged.

- Baseline: `4da23d040ca5bd6ffc7db75ce2c62be460f55493`.
- Baseline SHA-256: `90848e3fe3a3fb7eec8dea6d7a26098271debfd0cf029261d73459af41bbce88`.
- Defaults: Q4_K_M, 20 slots, 24,000 context budget and 20,000 maximum output.
- llama.cpp padding is verified: 24,064 actual tokens per slot for that configuration;
  the translator continues to budget against 24,000.
- Protocol v1 exposes authenticated runtime evidence and template/tokenizer budgets.
- Existing writer admission, lease, model locks and stream cleanup are retained.
- HTML v6 remains an optional diagnostic tool; StoryForge uses its existing translation engine.

Generate from the linked StoryForge Draft PR:

```powershell
python tools/personal-ai-concurrency/build_test_notebook.py --baseline tools/personal-ai-concurrency/fixtures/released-4da23d0.ipynb --output StoryForge-Translator-Personal-AI-20.ipynb --with-html
```

Open this notebook on its experimental Git ref, run the connection cell, then approve
the pairing code in StoryForge. Never copy an API key. Existing linked machines may
be reused. The final HTML diagnostic cell does not start translation automatically.

Local contract tests use simulated llama.cpp responses. Real GPU inference, memory
capacity, 20-slot throughput, public tunnel/CORS and long running behavior remain
unverified. Starting the notebook consumes the owner's Colab resources and is a
deliberate user action.
