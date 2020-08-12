

function download_java_large_model {
    wget https://s3.amazonaws.com/code2seq/model/java-large/java-large-model.tar.gz
    tar -C ../code2seq/. -xvzf java-large-model.tar.gz
    rm java-large-model.tar.gz
}

function download_java_small_dataset {
    wget https://s3.amazonaws.com/code2seq/datasets/java-small.tar.gz
    tar -C ../data/. -xvzf java-small.tar.gz
    rm java-small.tar.gz
}

read -p "Download Java-large model? (Y/N): " confirm && [[ $confirm == [yY] || $confirm == [yY][eE][sS] ]] && download_java_large_model
read -p "Download Java-large dataset? (Y/N): " confirm && [[ $confirm == [yY] || $confirm == [yY][eE][sS] ]] && download_java_small_dataset
