from flask import Flask
import pandas as pd
from flask import request,render_template
from werkzeug.utils import secure_filename
import os
app=Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def upload_file1():
    if request.method =="POST":
        f=request.files["f1"]
        option=request.form["s"]
        basepath=os.path.dirname(__file__)
        file_path=os.path.join(basepath,"uploads",secure_filename(f.filename))
        f.save(file_path)
        data=pd.read_csv(file_path)
        shape=data.shape
        coloum_null=list(data.isnull().any())
        coloum_name=list(data)
        for i in range(len(coloum_null)):
            if(coloum_null[i]):
                data[coloum_name[i]].fillna(data[coloum_name[i]].mode()[0],inplace = True)
        dl=[]
        for j in range(len(coloum_name)):
            dl.append((type(data[coloum_name[j]][1])))  
        dataarray=data.to_numpy()
        droplist=[]
        for k in range(len(dataarray)):
            for j in range(k+1,len(dataarray)):
                if(list(dataarray[k])==list(dataarray[j])):
                    droplist.append(j)
        data.drop(index=droplist,inplace=True)
        from sklearn.preprocessing import LabelEncoder
        le=LabelEncoder()
        for i in range(len(dl)):
            if dl[i]==str:
                data[coloum_name[i]]= le.fit_transform(data[coloum_name[i]])
        file_path_validated=os.path.join(basepath,"validated",secure_filename(f.filename))
        data.to_csv(file_path_validated)
        if(option=="Yes"):
            dataarray1=data.to_numpy()
            import numpy as np
            from sklearn.preprocessing import OneHotEncoder
            one=OneHotEncoder()
            z=[]
            index=[]
            for i in range(len(dl)):
                if dl[i]==str:
                    z.append(one.fit_transform(dataarray1[:,i:i+1]).toarray())
                    index.append(i)
            dataarray1=np.delete(dataarray1,index,axis=1)
            for j in range(len(z)):
                dataarray1=np.concatenate((z[j],dataarray1),axis=1) 
            from sklearn.preprocessing import StandardScaler
            sc=StandardScaler()
            dataarray1=sc.fit_transform(dataarray1)
            fpav=os.path.join(basepath,"validated","data",secure_filename(f.filename))
            np.savetxt(fpav,dataarray1,delimiter=",")
        return render_template("index.html",a1="Schema of the given csv file:",a2="No of row:"+str(shape[0]),
                               a3="No of coloum:"+str(shape[1]),a4="Name of the coloums:"+str(coloum_name),
                               a5="Corresponding datatype:"+str(dl),
                               a6="Your csv file is sucessfully validated and saved!")
if __name__=='__main__':
    app.run(debug=True)
    
    
    