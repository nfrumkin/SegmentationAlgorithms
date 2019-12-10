import pickle
import numpy as np
import PIL
from PIL import Image
from scipy.stats import multivariate_normal
import maxflow
import matplotlib.pyplot as plt
import math
import time

class Graph():
    def __init__(self, path, src_connections, sink_connections, lmbda=1, sigma = .00001):
        self.path = path
        self.lmbda = lmbda
        self.sigma = sigma
        self.src_conns = np.transpose(src_connections)
        self.sink_conns = np.transpose(sink_connections)
        self.png_to_array(path)
        self.g = maxflow.Graph[int]()
        self.nodes = self.g.add_nodes(self.length*self.width)

        self.create_neighbors()
        self.compute_conditional_probs()
        self.calculate_weights()

    def png_to_array(self,path):
        img_path = "imgs/cow.jpg"
        img = PIL.Image.open(img_path)
        grayscale_img = img.convert('LA')

        self.length = grayscale_img.size[0]
        self.width = grayscale_img.size[1]
        self.num_nodes = self.length*self.width
        self.img_mat = np.zeros([self.length, self.width])
        for i in range(self.length):
            for j in range(self.width):
                self.img_mat[i,j] = grayscale_img.getpixel((i,j))[0]

    
    def get_interpixel_weight(self, i1, j1, i2, j2):
        exponent = (self.img_mat[i1,j1] - self.img_mat[i2,j2])**2
        exponent = exponent * -.5/(self.sigma)**2
        return np.exp(exponent)
    
    def create_neighbors(self):
        # self.adj_matrix = np.zeros([self.num_nodes+2, self.num_nodes], dtype=float)
        for i in range(0,self.length):
            for j in range(0,self.width):
                if i > 0:
                    nd1 = i*self.width + j
                    nd2_i = i-1
                    nd2_j = j
                    nd2 = nd2_i*self.width+nd2_j
                    weight = self.get_interpixel_weight(i,j, nd2_i, nd2_j)
                    self.g.add_edge(nd1, nd2, weight, 0)
                    # self.adj_matrix[nd1, nd2] = self.get_interpixel_weight(i,j, nd2_i, nd2_j)
                elif i < self.width - 1:
                    nd1 = i*self.width + j
                    nd2_i = i+1
                    nd2_j = j
                    nd2 = nd2_i*self.width+nd2_j
                    weight = self.get_interpixel_weight(i,j, nd2_i, nd2_j)
                    self.g.add_edge(nd1, nd2, weight, 0)
                    # self.adj_matrix[nd1, nd2] = self.get_interpixel_weight(i,j, nd2_i, nd2_j)
                elif j > 0:
                    nd1 = i*self.width + j
                    nd2_i = i
                    nd2_j = j-1
                    nd2 = nd2_i*self.width+nd2_j
                    weight = self.get_interpixel_weight(i,j, nd2_i, nd2_j)
                    self.g.add_edge(nd1, nd2, weight, 0)
                    # self.adj_matrix[nd1, nd2] = self.get_interpixel_weight(i,j, nd2_i, nd2_j)
                elif j < self.length - 1:
                    nd1 = i*self.width + j
                    nd2_i = i
                    nd2_j = j+1
                    nd2 = nd2_i*self.width+nd2_j
                    weight = self.get_interpixel_weight(i,j, nd2_i, nd2_j)
                    self.g.add_edge(nd1, nd2, weight, 0)
                    # self.adj_matrix[nd1, nd2] = self.get_interpixel_weight(i,j, nd2_i, nd2_j)
        
    def compute_conditional_probs(self):
        self.mu_src = np.mean(self.src_conns, axis=0)
        self.cov_src = np.cov(self.src_conns, rowvar=False)
        self.mu_sink = np.mean(self.sink_conns, axis=0)
        self.cov_sink = np.cov(self.sink_conns, rowvar=False)
    
    def p_src(self, value):
        return multivariate_normal.pdf(value, mean=self.mu_src, cov=self.cov_src)
    
    def p_sink(self, value):
        return multivariate_normal.pdf(value, mean=self.mu_sink, cov=self.cov_sink)
        
    def calculate_weights(self):
        # src_weights = np.zeros([self.num_nodes,1])
        # sink_weights = np.zeros([self.num_nodes,1])
        for i in range(0,self.num_nodes):
            x_value = i / self.width
            y_value = i % self.width
            value = np.array([x_value, y_value])

            p_sink = self.p_sink(value)
            p_src = self.p_src(value)
            total_prob = p_sink + p_src
            # normalize
            p_sink = p_sink/total_prob
            p_src = p_src/total_prob
            # compute weights
            self.g.add_tedge(i,10*p_sink, 3*p_src)
            # src_weights[i] = -self.lmbda*np.log(p_sink)
            # sink_weights[i] = -self.lmbda*np.log(p_src)

        # for i in range(0,self.src_conns.shape[0]):
        #     node_number = self.src_conns[i,0]*self.width + self.src_conns[i,1]
        #     src_weights[node_number] = 1
        #     sink_weights[node_number] = 0
        
        # for i in range(0,self.sink_conns.shape[0]):
        #     node_number = self.sink_conns[i,0]*self.width + self.sink_conns[i,1]
        #     src_weights[node_number] = 0
        #     sink_weights[node_number] = 1
        
        # new_weights = np.vstack([np.transpose(src_weights), np.transpose(sink_weights)])
        # append sink/src weights to matrix   
        # print("stacking..")
        # self.adj_matrix[self.num_nodes,:] = np.transpose(src_weights)
        # self.adj_matrix[self.num_nodes+1,:] = np.transpose(sink_weights)

def read_annotations_pkl(src_path, sink_path):
    f = open(src_path, "rb")
    src_conns = pickle.load(f)
    f.close()

    f = open(sink_path, "rb")
    sink_conns = pickle.load(f)
    f.close()
    
    return src_conns, sink_conns

if __name__ == "__main__":
    img_path = "imgs/chicken.jpg"
    src_path = "src_conns.pkl"
    sink_path = "sink_conns.pkl"
    src_connections, sink_connections = read_annotations_pkl(src_path, sink_path)
    print("Generating Graph..")
    start = time.time()
    mygraph = Graph(img_path, src_connections, sink_connections)
    stop = time.time()
    print("elapsed: ", stop - start)
    # print(mygraph.adj_matrix)
    # f = open("adj_mat.pkl", "wb")
    # pickle.dump(mygraph.adj_matrix, f)
    # f.close()
    print("Computing Max Flow..")
    start = time.time()
    flow = mygraph.g.maxflow()
    stop = time.time()
    print("elapsed: ", stop - start)
    print("flow: ", flow)

    cuts = mygraph.g.get_grid_segments(mygraph.nodes)

    print("\n-Finding cut:")

    def get_pos_from_node_number(node_number):
        row=math.floor( float(node_number)/float(mygraph.width) )
        col=node_number%mygraph.width
        return (int(row),col)

    #forming new foreground image
    Iout = np.ones(shape = mygraph.nodes.shape)
    img = np.zeros([mygraph.length, mygraph.width])
    mask=np.zeros((mygraph.length,mygraph.width,1))
    for i in range(len(mygraph.nodes)):
        Iout[i] = mygraph.g.get_segment(mygraph.nodes[i]) # calssifying each pixel as either foreground or background
        if (Iout[i]==True):
            x,y=get_pos_from_node_number(i)
            img[x,y]=200
    img = np.transpose(img)

    plt.imshow(img,vmin=0,vmax=255) # plot the output image
    plt.show()