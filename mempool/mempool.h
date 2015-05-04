#include <stdlib.h>
#include <wtypes.h>

#define  MEMPOOL_ALIGNMENT 8            //对齐长度
//内存块，每个内存块管理一大块内存，包括许多分配单元
class MemoryBlock
{
public:
	MemoryBlock (int nUnitSize,int nUnitAmount);
	~MemoryBlock(){};
	static void*    operator new    (size_t,int nUnitSize,int nUnitAmount);
	static void     operator delete (void* ,int nUnitSize,int nUnitAmount){};
	static void     operator delete (void* pBlock);

	int             nSize;              //该内存块的大小，以字节为单位
	int             nFree;              //该内存块还有多少可分配的单元
	int             nFirst;             //当前可用单元的序号，从0开始
	MemoryBlock*    pNext;              //指向下一个内存块
	char            aData[1];           //用于标记分配单元开始的位置，分配单元从aData的位置开始

};

class MemoryPool
{
public:
	MemoryPool (int _nUnitSize,
		int _nGrowSize = 1024,
		int _nInitSzie = 256);
	~MemoryPool();
	void*           Alloc();
	void            Free(void* pFree);

private:
	int             nInitSize;          //初始大小
	int             nGrowSize;          //增长大小
	int             nUnitSize;          //分配单元大小
	MemoryBlock*    pBlock;             //内存块链表
};


#include <vector>

/*
	队列内存池：实现简单的定长内存缓存机制
	内存队列为空时则从物理内存中申请，并为继续增长预留空间，内存释放时不从物理内存释放，放入队列中

	注意：非线程安全
*/

class MemPool
{
public:
	MemPool(unsigned int alloc_size, unsigned int _increase, const char *class_name);
	~MemPool();

	void * Alloc();
	void Free(void *mem);

protected:
	void Increase();

private:
	MemPool(const MemPool &_m);
	MemPool & operator=(const MemPool &_r);

private:
	std::vector<void *> m_block_pool;
	std::vector<void *> m_malloc_record;

	unsigned int m_size;
	unsigned int m_size_for_increase;

	int m_record_index;
	const char *m_name;
};





#define REGISTER_MEMPOOL(PoolNameSpace, ClassName, INCREASE_NUM, ClassNameStr) \
namespace PoolNameSpace\
{\
	MemPool g_##ClassName##_mem_pool(sizeof(ClassName), INCREASE_NUM, ClassNameStr);\
}\
void *ClassName::operator new(size_t c)\
{\
	void *mem = PoolNameSpace::g_##ClassName##_mem_pool.Alloc();\
	return mem;\
}\
void ClassName::operator delete(void *m)\
{\
	PoolNameSpace::g_##ClassName##_mem_pool.Free(m);\
}

#define DEFINE_MEMPOOL\
void *	operator new(size_t c);\
void	operator delete(void *m);\


