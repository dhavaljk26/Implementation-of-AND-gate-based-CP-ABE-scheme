#include <bits/stdc++.h>
using namespace std;

#define RHO 8
#define NUM_ATTRIBUTE 4

long long P[NUM_ATTRIBUTE+2],Q[NUM_ATTRIBUTE+2];

bool checkPrime(long long randPrime)
{
	for(long long int i=2;i*i<=randPrime;i++)
	{
		if(randPrime%i==0)
			return false;
	}
	return true;
}

long long generatePrime(int rho){
	long long randPrime = 0;

	while(rho--){
		randPrime = 2*randPrime + (rand()%2) ;
	}
	
	randPrime |= ((1<<RHO) | 1);
	
	while(!checkPrime(randPrime)){
		// cout<<randPrime<<endl;
		randPrime+=2;
	}

	return randPrime;
}

long long getPhi(long long num){
	long long temp = num;
	long long ans=num;
	for (long long i=2;i*i<=num;i++){
		if(temp%i==0){
			ans*=(i-1);
			ans/=i;
			while(temp%i==0){
				temp/=i;
			}
		}
	}

	if(temp!=1){
		ans*=(temp-1);
		ans/=temp;
	}

	return ans;
}

long long power(long long a,long long b,long long mod){
	if(b==0)
		return 1;

	long long mid=power(a,b/2,mod);
	mid=(mid*mid)%mod;

	if(b%2)
		mid=(mid*a)%mod;
	return mid;
}

int main(){
	srand(time(0));
	long long p,q;
	p=generatePrime(RHO);
	q=p;

	while(p!=q){
		q=generatePrime(RHO);
	}

	long long N=p*q;
	cout<<"Public key is "<<N<<endl;

	long long phi=(p-1)*(q-1);
	cout<<"Phi "<< phi<<endl;
	set<long long >s;
	for (int i=0;i<NUM_ATTRIBUTE;i++){
		long long x=rand()%N+1;
		while(__gcd(x,phi)!=1 || s.find(x)!=s.end()){
			x=rand()%N+1;
		}
		s.insert(x);
	}
	long long phiphi=getPhi(phi);
	cout<<phiphi<<endl;
	int c=0;
	for (set<long long>::iterator it=s.begin();it!=s.end();it++){
		P[c]=*it;
		
		Q[c]=power(*it,phiphi-1,phi);
		cout<<P[c]<<" "<<Q[c]<<endl;
		c++;
	}

}