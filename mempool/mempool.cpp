#include "mempool.h"
#include <stdlib.h>
#include <memory.h>
#include <assert.h>


MemoryBlock::MemoryBlock( int nUnitSize,int nUnitAmount )
	:   nSize   (nUnitAmount * nUnitSize),
	nFree   (nUnitAmount - 1),  //构造的时候，就已将第一个单元分配出去了，所以减一
	nFirst  (1),                //同上
	pNext   (NULL)
{
	//初始化数组链表，将每个分配单元的下一个分配单元的序号写在当前单元的前两个字节中
	char* pData = aData;
	//最后一个位置不用写入
	for( int i = 1; i < nUnitAmount; i++)
	{
		(*(USHORT*)pData) = i;
		pData += nUnitSize;
	}
}

void* MemoryBlock::operator new(size_t, int nUnitSize,int nUnitAmount )
{
	return ::operator new( sizeof(MemoryBlock) + nUnitSize * nUnitAmount );
}

void MemoryBlock::operator delete( void* pBlock)
{
	::operator delete(pBlock);
}

MemoryPool::MemoryPool( int _nUnitSize, int _nGrowSize /*= 1024*/, int _nInitSzie /*= 256*/ )
{
	nInitSize = _nInitSzie;
	nGrowSize = _nGrowSize;
	pBlock = NULL;
	if(_nUnitSize > 4)
		nUnitSize = (_nUnitSize + (MEMPOOL_ALIGNMENT - 1)) & ~(MEMPOOL_ALIGNMENT - 1);
	else if( _nUnitSize < 2)
		nUnitSize = 2;
	else
		nUnitSize = 4;
}

MemoryPool::~MemoryPool()
{
	MemoryBlock* pMyBlock = pBlock;
	MemoryBlock* pNext = NULL;
	while( pMyBlock != NULL)
	{
		pNext = pMyBlock->pNext;
		delete(pMyBlock);
		pMyBlock = pNext;
	}
}

void* MemoryPool::Alloc()
{
	if( NULL == pBlock)
	{
		//首次生成MemoryBlock,new带参数，new了一个MemoryBlock类
		pBlock = (MemoryBlock*)new(nUnitSize,nInitSize) MemoryBlock(nUnitSize,nInitSize);
		return (void*)pBlock->aData;
	}

	//找到符合条件的内存块
	MemoryBlock* pMyBlock = pBlock;
	while( pMyBlock != NULL && 0 == pMyBlock->nFree )
		pMyBlock = pMyBlock->pNext;

	if( pMyBlock != NULL)
	{
		//找到了，进行分配
		char* pFree = pMyBlock->aData + pMyBlock->nFirst * nUnitSize;
		pMyBlock->nFirst = *((USHORT*)pFree);
		pMyBlock->nFree--;

		return (void*)pFree;
	}
	else
	{
		//没有找到，说明原来的内存块都满了，要再次分配

		if( 0 == nGrowSize)
			return NULL;

		pMyBlock = (MemoryBlock*)new(nUnitSize,nGrowSize) MemoryBlock(nUnitSize,nGrowSize);

		if( NULL == pMyBlock)
			return NULL;

		//进行一次插入操作
		pMyBlock->pNext = pBlock;
		pBlock = pMyBlock;

		return (void*)pMyBlock->aData;
	}
}

void MemoryPool::Free( void* pFree )
{
	//找到p所在的内存块
	MemoryBlock* pMyBlock = pBlock;
	MemoryBlock* PreBlock = NULL;
	while ( pMyBlock != NULL && ( pBlock->aData > pFree || pFree > pMyBlock->aData + pMyBlock->nSize))
	{
		PreBlock = pMyBlock;
		pMyBlock = pMyBlock->pNext;
	}

	if( NULL != pMyBlock )      //该内存在本内存池中pMyBlock所指向的内存块中
	{      
		//Step1 修改数组链表
		*((USHORT*)pFree) = pMyBlock->nFirst;
		pMyBlock->nFirst  = (USHORT)((ULONG)pFree - (ULONG)pMyBlock->aData) / nUnitSize;
		pMyBlock->nFree++;

		//Step2 判断是否需要向OS释放内存
		if( pMyBlock->nSize == pMyBlock->nFree * nUnitSize )
		{
			//在链表中删除该block

			delete(pMyBlock);
			if(PreBlock)
				PreBlock->pNext = NULL;
			else
				pBlock = NULL; 
		}
		else
		{
			//将该block插入到队首
			PreBlock = pMyBlock->pNext;
			pMyBlock->pNext = pBlock;
			pBlock = pMyBlock;
		}
	}
}


MemPool::MemPool(unsigned int alloc_size, unsigned int _increase, const char *class_name)
	:m_size(alloc_size), m_size_for_increase(_increase), m_record_index(-1), m_name(class_name)
{

}

MemPool::~MemPool()
{
	for (int i = 0; i < (int)m_malloc_record.size(); ++i)
	{
		::free(m_malloc_record[i]);

		// 这里无法统计释放，不过由于内存池一般都是全局性的，所以，此处的统计也就变得无关紧要了

		//#ifdef MEMORY_MONITOR
		//		long long increase_size = m_size * m_size_for_increase;
		//		memmonitor::AllocStat(-increase_size);
		//#endif

	}
}

void * MemPool::Alloc()
{
	void *mem = 0;

	if(m_block_pool.size() == 0)
	{
		Increase();
		if(m_block_pool.size() == 0)
		{
			return 0;
		}
	}

	mem = m_block_pool.back();
	m_block_pool.pop_back();

	return mem;
}

void MemPool::Free(void *mem)
{
	m_block_pool.push_back(mem);
}

void MemPool::Increase()
{
	size_t increase_size = m_size * m_size_for_increase;
	void *mem = ::malloc(increase_size);
	if (mem == 0) return ;

	m_malloc_record.push_back(mem);
	char *p = (char *)mem;
	for (unsigned int i = 0; i < m_size_for_increase; ++i, p += m_size)
	{
		m_block_pool.push_back((void *)p);
	}
}
