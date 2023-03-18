<h2>Dataset</h2>

You can find our dataset in `./data/`. This folder includes the following files:

<ul>
<li>

`./data/binaries.7z.link`: We used the same Wasm binaries that SnowWhite provided. For more info see <a href="https://github.com/sola-st/wasm-type-prediction">SnowWhite</a></li>


<li>

`./data/dataset.7z.link`: We used the same dataset that SnowWhite provided. For more info see <a href="https://github.com/sola-st/wasm-type-prediction">SnowWhite</a></li>
<li>

`./data/combined.7z.link`: This file contains a more compact version of the dataset introduced in SnowWhite. Bascially, we combined all the necessary information including labels for return type recovery and method name prediciton together, so we can only work with one training/test/dev file. This file is 23.2 MB and after decompression would be around 800 MB</li>

<li>

`./data/seqs.7z.link`: This file includes the different input sequences for different dataset variants for both return type recovery and method name prediciton. These sequences will be used directly as inputs to seq2seq models. There are 5 sequences per dataset variant:
<ol>
<li>seq1: nested-paths only (seq2seq-NP)</li>
<li>seq2: instructions only (seq2seq-I)</li>
<li>seq3: nested-paths and instructions concatenated (seq2seq-INP)</li>
<li>seq4: simple-paths only (seq2seq-SP)</li>
<li>seq5: simple-paths and instructions concatenated (seq2seq-ISP)</li>
</ol>
This file is 300 MB and after decompression would be around 8.65 GB.
</li>
<li>

`./data/embedding.7z`: This file contains feature vectors and their corresponding method name labels that we used to create Wasm code embeddings. The size of the file is 14 MB and after decompression would be around 4.5 GB.</li>
</ul>

We used this command for compression:
```
7z a <name>.7z <folder>
```

Use this for decompression:
```
7z x <name>.7z
```