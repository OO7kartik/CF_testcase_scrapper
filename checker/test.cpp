//testing file :p

#include <bits/stdc++.h>
using namespace std;

int main()
{

    freopen("Files/input.txt", "r", stdin);
    freopen("Files/output.txt", "a", stdout);

	 int n;
    cin>>n;
    if(n == 2)
    {
       cout<<"NO";
    }
    if(n % 2 ==  0 && n!=2)
    {
       cout<<"YES";
    }
    if(n % 2 != 0)
    {
       cout<<"NO";
    }
  	return 0;
}
