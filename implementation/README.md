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

`./run.py`: The multi-threaded program we used to convert wasm binaries in our dataset to path sequences.</li>

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
