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
