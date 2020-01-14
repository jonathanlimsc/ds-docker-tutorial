import numpy as np
import xgboost as xgb
from sklearn import datasets
import pickle
from utils import save_model, load_model

def randomize_data_labels(data, labels):
    assert len(data) == len(labels), "Dimensions of data and labels are different"
    random_indices = np.random.choice([i for i in range(data.shape[0])], size=data.shape[0], replace=False)
    data = data[random_indices]
    labels = labels[random_indices]
    return data, labels

def calculate_accuracy(pred, actual):
    correct = len(np.where(pred == actual)[0])
    return correct * 1. / len(pred) * 100

def generate_train_val_test_data():
    iris = datasets.load_iris()
    data, labels, target_names = iris['data'], iris['target'], iris['target_names']
    data, labels = randomize_data_labels(data, labels)
    train_val_test = [0.7, 0.1, 0.2]
    assert train_val_test[0] + train_val_test[1] + train_val_test[2] == 1.0, "Train val test ratios do not add to 1.0"

    num_train = int(train_val_test[0] * data.shape[0])
    num_val = int(train_val_test[1] * data.shape[0])
    num_test = data.shape[0] - num_train - num_val

    assert num_train + num_val + num_test == data.shape[0], "Train Val and Test data size != dataset size"

    train_X = data[:num_train]
    train_Y = labels[:num_train]
    val_X = data[num_train:num_train+num_val]
    val_Y = labels[num_train:num_train+num_val]
    test_X = data[num_train+num_val:]
    test_Y = labels[num_train+num_val:]

    return train_X, train_Y, val_X, val_Y, test_X, test_Y, target_names

if __name__ == '__main__':
    save_model_path = '../model/model.pkl'
    # Generate data
    train_X, train_Y, val_X, val_Y, test_X, test_Y, target_names = generate_train_val_test_data()
    print("Num Train: {}".format(len(train_X)))
    print("Num Val: {}".format(len(val_X)))
    print("Num Test: {}".format(len(test_X)))

    # Train model
    xgb_model = xgb.XGBClassifier(objective="multi:softprob", n_estimators=100)
    xgb_model.fit(train_X, train_Y)
    pred_val_Y = xgb_model.predict(val_X)
    val_acc = calculate_accuracy(pred_val_Y, val_Y)
    print("Validation accuracy: {}".format(val_acc))

    # Test accuracy
    pred_test_Y = xgb_model.predict(test_X)
    test_acc = calculate_accuracy(pred_test_Y, test_Y)
    print("Test accuracy: {}".format(test_acc))

    # Save model
    print("Saving model at {}".format(save_model_path))
    save_model(xgb_model, target_names, save_model_path)

    print("Training completed")
