#include <bits/stdc++.h>
using namespace std;

class Graph {
    int V;
    vector<pair<int, int>>* adj;
public:
    Graph(int V);
    void addEdge(int u, int v, int w);
    void uniformCost(int s, int f);
};
Graph::Graph(int V) {
    this->V = V;
    adj = new vector<pair<int, int>>[V];
}
void Graph::addEdge(int u, int v,int  w) {
    adj[u].push_back(pair<int, int> (v, w));
    adj[v].push_back(pair<int, int> (u, w));
}
class compare {
    public:
    bool operator () (pair<int, int> p1, pair<int, int> p2) {
        return p1.first < p2.first;
    }
};

void Graph::uniformCost(int s, int f) {
    priority_queue<pair<int, int>, vector<pair<int, int>>, compare> pq;
    vector<int> dist(V, INT32_MAX);
    vector<int> prev(V, -1);
    pq.push(pair<int, int> (0, s));
    dist[s] = 0;
    prev[s] = s;
    while(pq.size()) {
        int u = pq.top().second;
        pq.pop();
        for (auto i = adj[u].begin(); i != adj[u].end(); ++i) {
            int v = i->first;
            int weight = i->second;
            if (dist[v] > dist[u] + weight) {
                dist[v] = dist[u] + weight;
                prev[v] = u;
                pq.push(make_pair(dist[v], v));
            }
        }
    }
    cout<<"Shortest Distance: "<<dist[f]<<endl;
    cout<<"Shortest Path: \n";
    
    cout<<f<<"<-";
    int x = prev[f];
    while(1) {
        cout<<x<<"<-";
        x = prev[x];
        if(x == s)
            break;
    }
    cout<<s<<endl;
}

int main() {
    int V, E;
    cout<<"Enter the number of vertices: ";
    cin>>V;
    cout<<"Enter the number of edges: ";
    cin>>E;
    cout<<"Enter start, end and Edge respectively: \n";
    Graph g(V);
    for(int i = 0; i < E;i++) {
        int u, v, w;
        cin>>u>>v>>w;
        g.addEdge(u, v, w);
    }
    int s, f;
    cout<<"Enter the start and the end node: ";
    cin>>s>>f;
    g.uniformCost(s, f);
}
