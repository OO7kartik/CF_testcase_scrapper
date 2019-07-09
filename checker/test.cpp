//file that checks working of watermelon :p

#include <bits/stdc++.h>
using namespace std;
int main()
{

    freopen("Files/input.txt", "r", stdin);
    freopen("Files/output.txt", "a", stdout);

        long int kase,i,j,k,l,len,a,b;
        char str[10000],str1[1000];
        while(scanf("%ld",&kase)==1)
        {
        for(i=1;i<=kase;i++)
        {
            scanf("%s",&str);
            len=strlen(str);
            if(len<=10)
            {
                printf("%s\n",str);
            }
            else
            {
                printf("%c%d%c\n",str[0],len-2,str[len-1]);
            }
        }
        return 0;
    }
}
