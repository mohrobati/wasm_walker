
<h2>Results</h2>
You can find the results files of our evaluating our models for method name prediction and return type recovery in 

`./results/method_name` and `./results/type_pred`. Each log file includes prediction accuracy scores, BLEU scores, and other evaluation metrics. We used the script provided by SnowWhite authors to generate these metrics. You can find the script at `./results/eval.py`. The naming of the file indicates the dataset variant and input variant. For method name prediction, first token is the value of m and second token is the chosen input sequence. For instance, 20_seq3.pt is when m=20 and seq3 is chosen. For return type recovery, first token is the variant of dataset, similar to SnowWhite and second token is the chosen input sequence. 
