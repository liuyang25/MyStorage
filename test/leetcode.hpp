#pragma once
#include <vector>
#include <set>
#include <list>
#include <deque>
#include <stack>

#define NULL 0
#define uint32_t unsigned int
using namespace std;

int hammingWeight(unsigned int n) {
	int r = 0;
	while( n > 0 )
	{
		r += n % 2;
		n /= 2;
	}
	return r;
}

uint32_t reverseBits(uint32_t n) {
	uint32_t r = 0;
	int i = 0;
	while( n > 0 )
	{
		r <<=1;
		r += n % 2;
		n >>=1;
		++i;
	}
	i = 32 - i+1;
	while( --i > 0 )
		r <<=1;
	return r;
}

struct ListNode {
	int val;
	ListNode *next;
	ListNode(int x) : val(x), next(NULL) {}
};

ListNode *detectCycle(ListNode *head) {
	ListNode *hehe = head;
	ListNode *hehe2 = head;
	while(hehe != NULL)
	{
		if( hehe->next == hehe)
			return hehe;
		while(hehe2 != hehe)
		{
			if(hehe2== hehe->next)
				return hehe2;
			hehe2 = hehe2->next;
		}
		hehe2 = head;
		hehe = hehe->next;
	}
	return NULL;
}

bool largetstsort(const int& a, const int & b)
{

	return true;
}

//std::set<std::string, largetstsort> a;

std::string largestNumber(std::vector<int> &num)
{
	return "";
}

struct TreeNode {
	int val;
	TreeNode *left;
	TreeNode *right;
	TreeNode(int x) : val(x), left(NULL), right(NULL) {}
};

/*
     1						1\
	/ \						  2\
   2   5		to			    3\
  / \   \						 4\	
 3   4   6						  5\6 	 
*/
void flatten(TreeNode *root) {
	if (root == NULL)
		return;
	static std::list<TreeNode*> buff;
	if (root->right != NULL)
		buff.push_back(root->right);

	if( root->left != NULL )
		root->right = root->left;
	else if (buff.size() != 0)
	{
		root->right = buff.back();
		buff.pop_back();
	}
	root->left = NULL;
	flatten(root->right);;
}

//vector<vector<int> > threeSum(vector<int> &num) {
//	return 
//}
bool isChar(const char &x)
{
	if (x > 'z' || ( x < 'a' && x > 'Z') || x < 'A')
		return false;
	return true;
}
bool isNum(const char &x)
{
	if (x < '0' || x > '9')
		return false;
	return true;
}

bool isPalindrome(std::string s) {
	if( s.size() < 2 )
		return true;
	size_t rp = s.size() - 1;
	size_t lp = 0;
	char l,r;
	while (lp < rp)
	{
		l = s[lp]; r = s[rp];
		if (!isChar(l) && !isNum(l))
		{
			++lp;
			continue;
		}
		if (!isChar(r) && !isNum(r))
		{
			--rp;
			continue;
		}
		if( l == r || ( !isNum(l) && !isNum(r) && abs(l - r) == 32 ))
		{
			++lp; --rp;
			continue;
		}
		return false;
	}
	return true;
}

bool isChar(const char *x)
{
	if (*x > 'z' || ( *x < 'a' && *x > 'Z') || *x < 'A')
		return false;
	return true;
}
bool isNum(const char *x)
{
	if (*x < '0' || *x > '9')
		return false;
	return true;
}
bool isPalindromes(char *s) {
	int size = strlen(s)-1;
	if( size < 2 )
		return true;
	size_t rp = size - 1;
	size_t lp = 0;
	char l,r;
	while (lp < rp)
	{
		l = s[lp]; r = s[rp];
		if (!isChar(l) && !isNum(l))
		{
			++lp;
			continue;
		}
		if (!isChar(r) && !isNum(r))
		{
			--rp;
			continue;
		}
		if( l == r || ( !isNum(l) && !isNum(r) && abs(l - r) == 32 ))
		{
			++lp; --rp;
			continue;
		}
		return false;
	}
	return true;
}

/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     struct ListNode *next;
 * };
 */
struct ListNode *insertionSortList(struct ListNode *head) {
	if( head == NULL )
		return NULL;
	struct ListNode *mhead = NULL;

	struct ListNode *it = head;
	struct ListNode *next;
	int n = 0;
	while(it != NULL)
	{
		next = it->next;

		if( mhead == NULL )
		{
			mhead = it;
			it->next = NULL;
		}
		else if (mhead->val > it->val)
		{
			it->next = mhead;
			mhead = it;
		}
		else
		{
			struct ListNode *itt = mhead;
			while(itt != NULL)
			{
				if (itt->next == NULL)
				{
					itt->next = it;
					it->next = NULL;
					break;
				}
				else if(itt->next->val > it->val)
				{
					it->next = itt->next;
					itt->next = it;
					break;
				}
				else
				{
					itt = itt->next;
				}
			}
		}
		it = next;
	}

	return mhead;
}


/*
Given two integers n and k, return all possible combinations of k numbers out of 1 ... n.

	For example,
	If n = 4 and k = 2, a solution is:

[
	[2,4],
	[3,4],
	[2,3],
	[1,2],
	[1,3],
	[1,4],
]
*/
class Combine {
public:
	vector<vector<int> > combine(int n, int k) {
		result.clear();
		if (k == 0)
			return result;

		vector<int> prototype;
		for (int i = 1; i <= n - k + 1; ++i)
		{
			prototype.push_back(i);
			combine_in(prototype, i, n, k-1);
			prototype.pop_back();
		}
		return result;
	}
private:	
	vector<vector<int>> result;
	void combine_in(vector<int> &current, int l, int n, int k)
	{
		if (k == 0)
		{
			result.push_back(current);
			return;
		}

		for (int i = l+1; i <= n +1 - k; ++i)
		{
			current.push_back(i);
			combine_in(current, i, n, k-1);
			current.pop_back();
		}
	}
};

double Pow(double x, int n) {
	if (n == 0) return 1;
	if (n == 1) return x;
	if (n == -1) return 1/x;
	int next = n / 2;
	if (n < 0) next = 0 - next;
	double result = Pow( x * x,  next) * ((n % 2) ? x : 1);
	if (n < 0) result = 1/ result;
	return result;
}

vector<int> plusOne(vector<int>& digits) {
	int s = digits.size() - 1;
	while (s > 0)
	{
		if (digits[s] < 9)
		{
			digits[s] += 1;
			return digits;
		}
		else
		{
			digits[s] = 0;
			s -= 1;
		}
	}
	digits.insert(digits.begin(), 1);
	return digits;
}

/**
Given a binary tree, return the postorder traversal of its nodes' values.
 * Definition for binary tree
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode(int x) : val(x), left(NULL), right(NULL) {}
 * };
 */
class PostOrderTraversal {
public:
	void traversal(TreeNode *root)
	{
		if (root == NULL)
			return;
		m_queue.push(root->val);
		traversal(root->right);
		traversal(root->left);
	}
	vector<int> postorderTraversal(TreeNode *root) {
		traversal(root);
		vector<int> res;
		while (!m_queue.empty())
		{
			res.push_back(m_queue.top());
			m_queue.pop();
		}
		return std::move(res);
	}
	stack<int> m_queue;
};


class CountPrimes {
public:
	int countPrimes(int n)
	{
		int count = 0;
		int *bit = new int[n/32 + 1];
		memset(bit, 0, 4 * (n/32 + 1));
		for (int i = 2; i < n; ++i)
		{
			if ( (bit[i/32]  & (1 << (i%32))) != 0 )
				continue;
			++count;
			int j = i;
			while (j < n)
			{
				bit[j/32] |= (1 << (j%32));
				j += i;
			}
		}
		delete[] bit;

		return count;
	}
};

class RemoveElements {
public:
	ListNode* removeElements(ListNode* head, int val) {
		ListNode *pnode = head;
		ListNode *prev = NULL;
		while(pnode != NULL)
		{
			if (pnode->val == val)
			{
				if (prev == NULL)
					head = pnode->next;
				else
					prev->next = pnode->next;
			}
			else
			{
				prev = pnode;
			}
			pnode = pnode->next;
		}
		return head;
	}
};

class LRUCache{
public:
	LRUCache(int capacity) {
		m_capacity = capacity;
	}

	int get(int key) {
		auto it = m_index.find(key);
		if (it == m_index.end())
			return -1;
		
		int value = (*it->second)->value;
		m_data.push_back(*it->second);
		m_data.erase(it->second);
		m_index[key] = --m_data.end();
		return value;
	}

	void set(int key, int value) {
		if (m_capacity == 0)
			return;
		auto it = m_index.find(key);
		if (it != m_index.end())
		{
			auto &itr = it->second;
			(*itr)->value = value;
			m_data.push_back(*itr);
			m_data.erase(itr);
			m_index[key] = --m_data.end();
			return;
		}

		if (m_capacity == m_data.size())
		{
			Data* data = m_data.front();
			m_index.erase(data->key);
			m_data.pop_front();
			data->key = key;
			data->value = value;
			m_data.push_back(data);
			m_index[key] = --m_data.end();
			return;
		}

		Data *data = new Data;;
		data->key = key; data->value = value;
		m_data.push_back(data);
		m_index[key] = --m_data.end();
	}

private:
	struct Data
	{
		int key;
		int value;
	};
	int m_capacity;
	map<int, list<Data*>::iterator> m_index;
	list<Data*> m_data;
};

class IsIsomorphic {
public:
	bool isIsomorphic(string ab, string aa) {
		if (ab.length() != aa.length())
			return false;
		char l[256] = {};
		char r[256] = {};
		for (int i = 0; i < ab.length(); ++i)
		{
			if (l[ab[i]] == 0) 
				l[ab[i]] = aa[i];
			else if (l[ab[i]] != aa[i])
				return false;

			if (r[aa[i]] == 0) 
				r[aa[i]] = ab[i];
			else if (r[aa[i]] != ab[i])
				return false;
		}

		return true;
	}
};

class RangeBitwiseAnd {
public:

	int rangeBitwiseAnd(int m, int n) {
		int msb=0;

		int t = m ^ n;
		while (t >>= 1)
			msb++;
		unsigned int mask = ~((1 << msb) -1);

		return m & mask;
	}
};

class TwoSum {
public:
	vector<int> twoSum(vector<int>& nums, int target) {
		multimap<int,int> nummap;
		int i = 0;
		for(auto it:nums)
		{
			nummap.insert(pair<int,int>(it,i++));
		}
		vector<int> vnum;
		vnum.resize(nums.size());
		i = 0;
		for(auto it:nummap)
		{
			vnum[i++] = it.second;
		}
		vector<int> res;
		int l = 0;
		int r = 1;
		while ( r < nums.size())
		{
			if (nums[vnum[l]] + nums[vnum[r]] == target)
			{
				res.push_back(vnum[l] + 1);
				res.push_back(vnum[r] + 1);
				return res;
			}
			++r;
		}
		r -= 1;
		int temp; 
		while (l < r)
		{
			temp = nums[vnum[l]] + nums[vnum[r]];
			if (temp == target)
			{
				res.push_back(vnum[l] + 1);
				res.push_back(vnum[r] + 1);
				return res;
			}
			if (temp < target)
				++l;
			else
				--r;
		}
		return res;  
	}
};

class NumIslands {
public:
	int numIslands(vector<vector<char>> &grid) {

	}
};