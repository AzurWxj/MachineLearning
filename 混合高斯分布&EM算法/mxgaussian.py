import numpy as np
import matplotlib.pyplot as plt
import pickle,math

def generateData(configs,output):
    '''
    configs=[
        {
            'mean':Mean of the N-dimensional distribution,
            'cov':2-D array_like, of shape (N, N)
            'size':100
        },{...}
    ]
    @return 在config中的每个对象中添加一个data字段，size-dimensional
    '''
    for config in configs:
        if('size' not in config):
            config['size']=100
        config['data']=np.random.multivariate_normal(mean=config['mean'],cov=config['cov'],size=config['size'])
    with open(output,mode='wb') as pklWriter:
        pickle.dump(configs,pklWriter)
    return configs

def loadData(fpath):
    with open(fpath,mode='rb') as reader: 
        answer=pickle.load(reader)
    return answer

PI2=2*np.pi

def gaussian(y,mean,sigma):
    '''
    y: m个分量，np.shape(m)
    mean: m个分量，np.shape(m)
    sigma: m*m协方差矩阵，np.shape(m,m)
    '''
    m,delta=y.shape[0],y-mean
    qform=np.dot(np.dot(delta,np.linalg.inv(sigma)),delta.reshape(m,1))
    return np.exp(-0.5*qform)/(
        (PI2**(m/2))*np.sqrt(np.linalg.det(sigma))
    )

def mxgaussian(y,k,phi,steps=10):
    '''
    y: np.shape(n,m) n个数据，每个数据m个分量
    k: 混合的高斯模型个数
    steps：迭代次数
    phi：np.shape(k)
    '''
    n,m = y.shape
    excep = np.zeros((n,k))
    means = np.random.randn(k,m)
    sigmas = np.array([np.eye(m) for _ in range(k)])
    yield means,sigmas,phi
    for _step in range(steps):
        #更新期望矩阵
        for _i in range(n):
            for _j in range(k):
                excep[_i,_j]=phi[_j] * gaussian(y[_i],means[_j],sigmas[_j])
            excep[_i]=excep[_i]/np.sum(excep[_i])
        #更新比例系数，但是先不除以n
        phi=excep.sum(axis=0)
        #先更新协方差矩阵
        for _j in range(k):
            delta=y[0]-means[_j]
            sigmas[_j]=excep[0,_j]*np.multiply(
                delta.reshape(-1,1),delta
            )
            for _i in range(1,n):
                delta=y[_i]-means[_j]
                sigmas[_j]=sigmas[_j]+excep[_i,_j]*np.multiply(
                    delta.reshape(-1,1),delta
                )
            sigmas[_j]=sigmas[_j]/phi[_j]
        #更新期望
        for _j in range(k):            
            means[_j]=(y*excep[:,_j].reshape(-1,1)).sum(axis=0)/phi[_j]
        phi=phi/n
        yield means,sigmas,phi

def _fitmxgaussian(x,means,sigmas,phi):
    vecGaussian=np.vectorize(lambda x: gaussian(np.array([x]),means[0],sigmas[0]))
    y=vecGaussian(x)*phi[0]
    for _i in range(1,phi.shape[0]):
        vecGaussian=np.vectorize(lambda x: gaussian(np.array([x]),means[_i],sigmas[_i]))
        y=y+vecGaussian(x)*phi[_i]
    return y

if __name__ == "__main__":
    '''
    answer=generateData([
        {
            'mean':np.array([6]),
            'cov':np.array([[5.5]]),
        },
        {
            'mean':np.array([-10]),
            'cov':np.array([[4.3]]),
        }
    ],'normaldata.pkl')
    '''
    answer=loadData('normaldata.pkl')
    x=np.linspace(-15,15,200)
    phi=[]
    y=np.array([phi.append(ans['size']) or ans['data'] for ans in answer]).reshape(-1,1)
    phi=np.array(phi)/np.sum(phi)
    cnt=1

    for cnt in range(1,1+len(answer)):
        with open("samples-%d.csv"%cnt,mode='w') as writer:
            for _y in answer[cnt-1]['data']:
                writer.write(str(_y[0])+"\n")
    
    for means,sigmas,phi in mxgaussian(y,k=2,phi=phi):
        with open("model-%d.csv"%cnt,mode='w') as writer:
            for _x,_y in zip(x,_fitmxgaussian(x,means,sigmas,phi)):
                writer.write(str(_x)+","+str(_y)+"\n")
        cnt+=1
    
    
    for cnt in range(1,1+len(answer)):
        with open("grdtrh-%d.csv"%cnt,mode='w') as writer:
            for _x,_y in zip(x,_fitmxgaussian(
                x,
                answer[cnt-1]['mean'].reshape(1,-1),
                answer[cnt-1]['cov'].reshape(1,answer[cnt-1]['cov'].shape[0],-1),
                np.array([[1]]))
            ):
                writer.write(str(_x)+","+str(_y)+"\n")

    #plt.scatter(y_,np.zeros_like(y_))
    