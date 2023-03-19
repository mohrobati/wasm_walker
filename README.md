<h1>WasmWalker: Path-based Code Representations for Improved WebAssembly Program Analysis</h1>

This repository houses the official replication package for the paper titled "WasmWalker: Path-based Code Representations for Improved WebAssembly Program Analysis". The package contains the following components:

<ul>

<li>Dataset: We have utilized the WebAssembly (wasm) binaries compiled by <a href="https://github.com/sola-st/wasm-type-prediction">SnowWhite</a> to generate two path-based code representations. After processing the dataset using our pipeline, we have obtained a new dataset that we have used for training our models. This replication package includes both our new dataset and SnowWhite's dataset.</li>

<li>Pipeline: Our pipeline has been designed to extract path sequences from Wasm binaries. We implemented our pipeline using Rust and Python.</li>

<li>Data cleaning: These scripts enable the splitting of the dataset into different variants and the creation of different input sequences.</li>

<li>Training notebooks: We have included two Jupyter notebooks, one for training a feed-forward neural network for creating code embeddings for method names, and the other for training seq2seq models with five different variants of input sequences.</li>

<li>Models: This section includes the weights of the seq2seq models trained using OpenNMT and the feedforward neural network used to generate the code embeddings.</li>

<li>Results: The log files in this section contain the evaluation results of our models, including prediction accuracy scores, BLEU scores, and other evaluation metrics.</li>

</ul>

We welcome contributions to improve our method. Please open an issue or submit a pull request.

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

<h2>Pipeline</h2>
You can find the code for our path extraction/processing pipeline (WasmWalker) in 

`./implementation/extraction`.
This folder includes the following:
<ul>
<li>

`./paths_set/`: This folder includes the empricial results of our path extraction step. `./paths_set/loop_if_collapsed.log` shows the 3352 refined paths mentioned in our paper.</li>

<li>

`./accumulate.py`: The single-threaded program we used to collect the accumulative disribution of refined paths within our dataset.</li>

<li>

`./collect.py`: The multi-threaded program we used to collect the raw paths within our dataset.</li>

<li>

`./run.py`: The multi-threaded program we used to convert wasm binaries in our dataset to path sequences. To reproduce the preprocessing step, you'd need to extract `./data/combined.7z.link` and `./data/binaries.7z.link` and change the paths accordingly.</li>

<li>

`./to_wat.py`: This file runs the Rust project at the root folder to use WABT::wasm2wat and store wat files in ./__ logs __/</li>

<li>

`./path.py`: DFS for collecting paths and the refinement algorithm are implemented here</li>
</ul>


<h2>Data Cleaning</h2>
The scripts we used to clean the data and split them into dataset variants and also provide different input sequences for each of them for method name prediction and return type recovery can be found at 

`./implementation/scripts/method-name` and `./implementation/scripts/type-pred`, respectively.

<h2>Training Notebooks</h2>

To faciliate the process of reproducing our results, we provide the Jupyter Notebooks that we used on Google Colab to train our models. The notebook that we used to create code embeddings can be found at `./implementation/scripts/training/embedding.ipynb`. For training our seq2seq models for both method name prediction and return type recovery, we used the notebook provided at `./implementation/scripts/training/OpenNMT.ipynb`. These files include all the necessary config information that can be helpful for replicating our results.

<h3>Steps for reproducing the embedding map</h3>

<ul>
<li>

Extract `./data/embedding.7z`, then copy `./names.txt` and `./vectors.txt` to your working directory.</li>

<li>

Extract `./models/models.7z`, then copy `./embedding.h5` to your working directory. Alternatively, you can not use this file, and retrain the feedforward-NN. The code for training is provided in the notebook (it's commented).</li>

<li>

Change the paths in `./implementation/scripts/training/embedding.ipynb` accordingly.</li>

<li>

Run code blocks in the jupyter notebook. The versions of the used packages are as follows: sklearn (1.2.2), keras (2.11.0), pandas (1.4.4), numpy (1.22.4).</li>

<li>

The generated embedding map will have overlapped labels, to separate them, uncomment the commented lines in the last code block.</li>
</ul>

<h3>Steps for reproducing the seq2seq models</h3>

<ul>
<li>

Extract `./data/seqs.7z.link`, then copy everything to your working directory.</li>

<li>

Extract `./models/models.7z`, then copy everything to your working directory.</li>

<li>

Change the paths in `./implementation/scripts/training/OpenNMT.ipynb` accordingly. The main path that you have to change is in the fifth code block:
```
import torch

torch.cuda.is_available()
torch.cuda.get_device_name(0)
folder = "path/to/sequences"
# EXAMPLE: folder = "./seqs/type_pred/eklavya/seq1" // to reproduce results for seq2seq-NP model for eklavya variant
```

</li>

<li>

If you want to retrain the seq2seq network then keep the code block containing the following command:

```
# Train the NMT model

!onmt_train -config config.yaml
```
If not, then comment this block and run the next blocks. Just remember to replace `--model='./model_best.pt'` with the path to the model you want from `./models/models.7z`.
</li>
</ul>

<h2>Models</h2>
You can find the weights for neural models that we trained in 

`./models/models.7z`. The size of the file is 4.41 MB and after decompression would be around 5.07 GB. After decompression you'd find the weights of seq2seq models for different variants and different input sequences for both method name prediction and return type recovery in `./models/method_name/` and `./models/type_pred/`. The models are generated using OpenNMT (.pt files). The naming of the file indicates the dataset variant and input variant. For method name prediction, first token is the value of m and second token is the chosen input sequence. For instance, 20_seq3.pt is when m=20 and seq3 is chosen. m is the minimum number of datapoints associated with a method name for it to be included in the dataset. For instance, if
a dataset is created with m = 50, that means each method name in the dataset has at least 50 datapoints associated with itself. For return type recovery, first token is the variant of dataset, similar to SnowWhite and second token is the chosen input sequence. 

In addition to the seq2seq weights, you'd find `./embedding.h5` which is the weights of the keras feedforward NN we used for creating code embeddings.

<h2>Results</h2>
You can find the results files of our evaluating our models for method name prediction and return type recovery in 

`./results/method_name` and `./results/type_pred`. Each log file includes prediction accuracy scores, BLEU scores, and other evaluation metrics. We used the script provided by SnowWhite authors to generate these metrics. You can find the script at `./results/eval.py`. The naming of the file indicates the dataset variant and input variant. For method name prediction, first token is the value of m and second token is the chosen input sequence. For instance, 20_seq3.pt is when m=20 and seq3 is chosen. For return type recovery, first token is the variant of dataset, similar to SnowWhite and second token is the chosen input sequence. 
