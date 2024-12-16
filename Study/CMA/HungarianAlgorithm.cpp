#include <cassert>
#include <iostream>
#include <limits>
#include <vector>
#include <climits>
using namespace std;

#define inf INT_MAX

bool checkMin(int &a, const int &b) { return b < a ? a = b, 1 : 0; }

vector<int> finalJobs;

vector<int> hungarian(const vector<vector<int>> &C) 
{
    const int J = (int)size(C), W = (int)size(C[0]);

    assert(J <= W);

    vector<int> job(W + 1, -1);     // job[w] = job assigned to w-th worker, or -1 if no job assigned
    vector<int> ys(J), yt(W + 1);     // potentials  ;;;;; -yt[W] will equal the sum of all deltas
    
    vector<int> answers;

    for (int j_cur = 0; j_cur < J; ++j_cur)    // assign j_cur-th job
    {
        int w_cur = W;              // Assigning current worker as 'auxillary worker'
        job[w_cur] = j_cur;
        
        // Let Z denote the alternating path in the graph 

        vector<int> min_to(W + 1, inf);     // min reduced cost over edges from Z to worker w
        vector<int> prv(W + 1, -1);         // previous worker on alternating path
        vector<bool> in_Z(W + 1);           // whether worker is in Z
        while (job[w_cur] != -1)           // runs at most j_cur + 1 times
        {
            in_Z[w_cur] = true;
            const int j = job[w_cur];
            int delta = inf;
            int w_next;
            for (int w = 0; w < W; ++w) {
                if (!in_Z[w]) {
                    if (checkMin(min_to[w], C[j][w] - ys[j] - yt[w]))
                        prv[w] = w_cur;
                    if (checkMin(delta, min_to[w])) w_next = w;
                }
            }
            
            for (int w = 0; w <= W; ++w) {
                if (in_Z[w]) ys[job[w]] += delta, yt[w] -= delta;
                else min_to[w] -= delta;
            }
            w_cur = w_next;
        }

        // update assignments along alternating path
        for (int w; w_cur != W; w_cur = w) job[w_cur] = job[w = prv[w_cur]];
        answers.push_back(-yt[W]);
    }
    finalJobs = job;
    return answers;
}

int main() 
{
    vector<vector<vector<int>>> costs {{{8,5,9},{4,2,4},{7,3,8}},
                                           {{40,25,55},{60,30,30},{15,45,25}},
                                           {{30,15,25},{25,10,20},{10,20,15}},
                                           {{16,5,8,3},{2,13,6,4},{3,7,5,5},{7,5,9,11}},
                                           {{4,8,12,6},{2,3,5,3},{5,10,4,7},{7,8,5,14}}};

    cout << "Delta values for said example: " << endl;
    auto ans = hungarian(costs[4]);
    for(auto& i:ans)
        cout << i << " ";
    for(int i = 0; i<size(finalJobs)-1; i++)
    {
        cout << "\nPerson " << i+1 << " works on job #" << finalJobs[i]+1 << ".";
    }
    cout << "\n\nTotal assignment cost = " << ans[size(ans)-1] << "\n\n";
    assert((hungarian(costs[0]) == vector<int>{5,9,15}));
    assert((hungarian(costs[1]) == vector<int>{25,55,70}));
    assert((hungarian(costs[2]) == vector<int>{15,35,45}));
    assert((hungarian(costs[3]) == vector<int>{3,5,10,15}));
    assert((hungarian(costs[4]) == vector<int>{4,7,11,19}));
    cerr << "\nAll assertions Passed\n";

    return 0;
}