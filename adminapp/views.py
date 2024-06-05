from django.shortcuts import render,redirect
from userapp.models import User
from adminapp.models import Dataset
import pandas as pd
from xgboost import XGBRegressor
# from sklearn.tree import DecisionTreeClassifier 
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from django.contrib import messages
import math




def index(request):
    t_users = User.objects.all()
    a_users = User.objects.filter(status="Accepted")
    p_users = User.objects.filter(status="Verified")
    context ={
        't_users':len(t_users),
        'a_users':len(a_users),
        'p_users':len(p_users),

    }
    return render(request,'admin/index.html',context)



def all_users(request):
    user = User.objects.filter(status = "Accepted")
    context = {
        'user':user,
    }
    return render(request,'admin/all-users.html',context)



def attacks_analysis(request):
    # datasets = Dataset.objects.all()
    # data_list = []
    # for dataset in datasets:
    #     df = pd.read_csv(dataset.file)
    #     protocol_counts = df['Attack Type'].value_counts()
    #     normal = protocol_counts.get('normal', 0)
    #     print(normal)
    #     dos = protocol_counts.get('dos', 0)
    #     print(dos)
    #     probe = protocol_counts.get('probe', 0)
    #     print(probe)
    #     r2l = protocol_counts.get('r2l', 0)
    #     print(r2l)
    #     u2r = protocol_counts.get('u2r', 0)
    #     print(u2r)

    #     data_list.append({
    #         'title': dataset.title,
    #         'normal': normal,
    #         'dos': dos,
    #         'probe': probe,
    #         'r2l': r2l,
    #         'u2r': u2r,

    #     })

    return render(request, 'admin/attacks-analysis.html')







def upload_dataset(request):
    if request.method == 'POST':
        csv_file = request.FILES.get('file') 
        if csv_file:
            Dataset.objects.all().delete()
            dataset = Dataset(title=csv_file.name, file=csv_file)
            dataset.save()
            return redirect('view_dataset')
    return render(request,'admin/upload-dataset.html')



def view_dataset(request):
    datasets = Dataset.objects.all()
    data_list = []
    
    for dataset in datasets:
        df = pd.read_csv(dataset.file)
        # df = df.head(1000)
        data = df.to_html(index=False)
        data_list.append({
            'title': dataset.title,
            'data': data
        })
        dataset.save()
    return render(request,'admin/view-dataset.html',{'data_list': data_list})


def pending_users(request):
    user = User.objects.filter(status = "Verified")
    print(user)
    context = {
        'user':user,
    }
    return render(request,'admin/pending-users.html',context)


def alg1(request):
    dataset = Dataset.objects.first() 
    df = pd.read_csv(dataset.file)
    print(df.columns)

    target_column = "Chance of Admit "  
    y = df['Chance of Admit ']
    X = df.drop(columns=['Chance of Admit '])
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    xgb_model = XGBRegressor(random_state=42, learning_rate=0.1, max_depth=6, n_estimators=100)
    xgb_model.fit(X_train, y_train)
    
    y_pred = xgb_model.predict(X_test)
    
    r2 = r2_score(y_test, y_pred)
    
    mse = mean_squared_error(y_test, y_pred)
    
    rmse = mean_squared_error(y_test, y_pred, squared=False)
    
    amse = mean_absolute_error(y_test, y_pred)
    
    request.session['XGBRegressor_R2'] = r2
    request.session['XGBRegressor_RMSE'] = rmse
    request.session['XGBRegressor_MSE'] = mse
    request.session['XGBRegressor_AMSE'] = amse


    metrics_data = {
        'algorithm': 'XGBRegressor',
        'R2_Score': r2,
        'RMSE': rmse,
        'MSE': mse,
        'AMSE': amse,
    }

    context = {
        'dataset_title': dataset.title,
        'target_column': target_column,
        'metrics_data': metrics_data,
    }
    
    return render(request, 'admin/algorithm-one.html', context)






def alg2(request):
    dataset = Dataset.objects.first() 
    df = pd.read_csv(dataset.file)
    print(df.columns)

    target_column = "Chance of Admit "  
    y = df['Chance of Admit ']
    X = df.drop(columns=['Chance of Admit '])
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    dt_model = DecisionTreeRegressor(random_state=42, max_depth= 7)
    dt_model.fit(X_train, y_train)
    y_pred = dt_model.predict(X_test)

    print(y_pred)

    r2 = r2_score(y_test, y_pred)
    
    mse = mean_squared_error(y_test, y_pred)
    
    rmse = mean_squared_error(y_test, y_pred, squared=False)
    
    amse = mean_absolute_error(y_test, y_pred)
    
    
    request.session['DecisionTreeRegressor'] = r2

    metrics_data = {
        'algorithm': 'DecisionTreeRegressor',
        'R2_Score': r2,
        'RMSE': rmse,
        'MSE': mse,
        'AMSE': amse,
    }

    context = {
        'dataset_title': dataset.title,
        'target_column': target_column,
        'metrics_data': metrics_data,
    }
    return render(request,'admin/algorithm-two.html',context)



def alg3(request):
    dataset = Dataset.objects.first() 
    df = pd.read_csv(dataset.file)
    print(df.columns)
    target_column = "Chance of Admit "  
    y = df['Chance of Admit ']
    X = df.drop(columns=['Chance of Admit '])
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    rfr = RandomForestRegressor(random_state=42, max_depth=7, n_estimators=128)
    rfr.fit(X_train, y_train)

    y_pred = rfr.predict(X_test)
    
    r2 = r2_score(y_test, y_pred)
    
    mse = mean_squared_error(y_test, y_pred)
    
    rmse = mean_squared_error(y_test, y_pred, squared=False)
    
    amse = mean_absolute_error(y_test, y_pred)
    
    

    request.session['RandomForestRegressor'] = r2

    metrics_data = {
        'algorithm': 'RandomForestRegressor',
        'R2_Score': r2,
        'RMSE': rmse,
        'MSE': mse,
        'AMSE': amse,
    }

    context = {
        'dataset_title': dataset.title,
        'target_column': target_column,
        'metrics_data': metrics_data,
    }
    return render(request, 'admin/algorithm-three.html',context)




def alg4(request):
    dataset = Dataset.objects.first() 
    df = pd.read_csv(dataset.file)
    print(df.columns)
    target_column = "Chance of Admit "  
    y = df['Chance of Admit ']
    X = df.drop(columns=['Chance of Admit '])
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    gbc = GradientBoostingRegressor(random_state=42, learning_rate=0.1, n_estimators=256, subsample=0.75)
    gbc.fit(X_train, y_train)
    y_pred = gbc.predict(X_test)

    r2 = r2_score(y_test, y_pred)
    
    mse = mean_squared_error(y_test, y_pred)
    
    rmse = mean_squared_error(y_test, y_pred, squared=False)
    
    amse = mean_absolute_error(y_test, y_pred)
    
    

    request.session['GradientBoostingRegressor'] = r2

    metrics_data = {
        'algorithm': 'GradientBoostingRegressor',
        'R2_Score': r2,
        'RMSE': rmse,
        'MSE': mse,
        'AMSE': amse,
    }

    context = {
        'dataset_title': dataset.title,
        'target_column': target_column,
        'metrics_data': metrics_data,
    }
    return render(request,'admin/algorithm-four.html',context)



def alg5(request):
    dataset = Dataset.objects.first() 
    df = pd.read_csv(dataset.file)
    print(df.columns)
    target_column = "Chance of Admit "  
    y = df['Chance of Admit ']
    X = df.drop(columns=['Chance of Admit '])
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    knr = KNeighborsRegressor( n_neighbors=7)
    knr.fit(X_train, y_train)
    y_pred = knr.predict(X_test)

    r2 = r2_score(y_test, y_pred)
    
    mse = mean_squared_error(y_test, y_pred)
    
    rmse = mean_squared_error(y_test, y_pred, squared=False)
    
    amse = mean_absolute_error(y_test, y_pred)
    
    

    request.session['KNeighborsRegressor'] = r2

    metrics_data = {
        'algorithm': 'KNeighborsRegressor',
        'R2_Score': r2,
        'RMSE': rmse,
        'MSE': mse,
        'AMSE': amse,
    }

    context = {
        'dataset_title': dataset.title,
        'target_column': target_column,
        'metrics_data': metrics_data,
    }
    return render(request, 'admin/algorithm-five.html',context)




def alg6(request):
    dataset = Dataset.objects.first() 
    df = pd.read_csv(dataset.file)
    print(df.columns)
    target_column = "Chance of Admit "  
    y = df['Chance of Admit ']
    X = df.drop(columns=['Chance of Admit '])
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    lr = LinearRegression()
    lr.fit(X_train, y_train)

    y_pred = lr.predict(X_test)

    r2 = r2_score(y_test, y_pred)
    
    mse = mean_squared_error(y_test, y_pred)
    
    rmse = mean_squared_error(y_test, y_pred, squared=False)
    
    amse = mean_absolute_error(y_test, y_pred)
    
    request.session['LinearRegression'] = r2
    

    metrics_data = {
        'algorithm': 'LinearRegression',
        'R2_Score': r2,
        'RMSE': rmse,
        'MSE': mse,
        'AMSE': amse,
    }

    context = {
        'dataset_title': dataset.title,
        'target_column': target_column,
        'metrics_data': metrics_data,
    }
    return render(request, 'admin/algorithm-six.html',context)




def alg7(request):
    dataset = Dataset.objects.first() 
    df = pd.read_csv(dataset.file)
    print(df.columns)
    target_column = "Chance of Admit "  
    y = df['Chance of Admit ']
    X = df.drop(columns=['Chance of Admit '])
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    svm_regressor = SVR()

    svm_regressor.fit(X_train, y_train)
    y_pred = svm_regressor.predict(X_test)

    r2 = r2_score(y_test, y_pred)
    
    mse = mean_squared_error(y_test, y_pred)
    
    rmse = mean_squared_error(y_test, y_pred, squared=False)
    
    amse = mean_absolute_error(y_test, y_pred)
    
    request.session['svm_regressor'] = r2
    

    metrics_data = {
        'algorithm': '',
        'R2_Score': r2,
        'RMSE': rmse,
        'MSE': mse,
        'AMSE': amse,
    }

    context = {
        'dataset_title': dataset.title,
        'target_column': target_column,
        'metrics_data': metrics_data,
    }
    return render(request, 'admin/algorithm-seven.html',context)



def graph_analysis(request):
    XGBRegressor_R2 = request.session.get('XGBRegressor_R2')
    print(XGBRegressor_R2)
    DecisionTree_accuracy = request.session.get('DecisionTreeRegressor')
    print(DecisionTree_accuracy)
    RandomForest_accuracy = request.session.get('RandomForestRegressor')
    print(RandomForest_accuracy)
    GradientBoostingRegressor = request.session.get('GradientBoostingRegressor')
    print(GradientBoostingRegressor)
    KNeighborsRegressor = request.session.get('KNeighborsRegressor')
    print(KNeighborsRegressor)
    LinearRegression_accuracy = request.session.get('LinearRegression')
    print(LinearRegression_accuracy)
    svm_regressor = request.session.get('svm_regressor')
    print(svm_regressor)

    if (
        XGBRegressor_R2 is None or
        DecisionTree_accuracy is None or
        RandomForest_accuracy is None or
        GradientBoostingRegressor is None or
        KNeighborsRegressor is None or
        LinearRegression_accuracy is None or
        svm_regressor is None
    ):
        messages.info(request, "Run all 7 algorithms before going to the graph")
        return redirect('alg1')

    formatted_XGBRegressor_R2 = "{:.2f}".format(math.floor(float(XGBRegressor_R2) * 100) / 100)
    formatted_DecisionTree_accuracy = "{:.2f}".format(math.floor(float(DecisionTree_accuracy) * 100) / 100)
    formatted_RandomForest_accuracy = "{:.2f}".format(math.floor(float(RandomForest_accuracy) * 100) / 100)
    formatted_GradientBoosting_accuracy = "{:.2f}".format(math.floor(float(GradientBoostingRegressor) * 100) / 100)
    formatted_KNeighbors_accuracy = "{:.2f}".format(math.floor(float(KNeighborsRegressor) * 100) / 100)
    formatted_LinearRegression_accuracy = "{:.2f}".format(math.floor(float(LinearRegression_accuracy) * 100) / 100)
    formatted_svm_regressor = "{:.2f}".format(math.floor(float(svm_regressor) * 100) / 100)

    context = {
        'XGBRegressor_R2': formatted_XGBRegressor_R2,
        'DecisionTree_accuracy': formatted_DecisionTree_accuracy,
        'RandomForest_accuracy': formatted_RandomForest_accuracy,
        'GradientBoosting_accuracy': formatted_GradientBoosting_accuracy,
        'KNeighbors_accuracy': formatted_KNeighbors_accuracy,
        'LinearRegression_accuracy': formatted_LinearRegression_accuracy,
        'svm_regressor': formatted_svm_regressor,
    }

    return render(request, 'admin/graph-analasis.html', context)





def accept_user(request,user_id):
    user = User.objects.get(user_id=user_id)
    user.status = 'Accepted'
    user.save()
    return redirect('pending_users')

def reject_user(request,user_id):
    user = User.objects.get(user_id = user_id)
    user.delete()
    return redirect('pending_users')


def delete_user(request,user_id):
    user = User.objects.get(user_id = user_id)
    user.delete()
    return redirect('all_users')

