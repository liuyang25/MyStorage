#include "mempool.h"
#include <stdlib.h>
#include <memory.h>
#include <assert.h>


MemoryBlock::MemoryBlock( int nUnitSize,int nUnitAmount )
	:   nSize   (nUnitAmount * nUnitSize),
	nFree   (nUnitAmount - 1),  //�����ʱ�򣬾��ѽ���һ����Ԫ�����ȥ�ˣ����Լ�һ
	nFirst  (1),                //ͬ��
	pNext   (NULL)
{
	//��ʼ������������ÿ�����䵥Ԫ����һ�����䵥Ԫ�����д�ڵ�ǰ��Ԫ��ǰ�����ֽ���
	char* pData = aData;
	//���һ��λ�ò���д��
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
		//�״�����MemoryBlock,new��������new��һ��MemoryBlock��
		pBlock = (MemoryBlock*)new(nUnitSize,nInitSize) MemoryBlock(nUnitSize,nInitSize);
		return (void*)pBlock->aData;
	}

	//�ҵ������������ڴ��
	MemoryBlock* pMyBlock = pBlock;
	while( pMyBlock != NULL && 0 == pMyBlock->nFree )
		pMyBlock = pMyBlock->pNext;

	if( pMyBlock != NULL)
	{
		//�ҵ��ˣ����з���
		char* pFree = pMyBlock->aData + pMyBlock->nFirst * nUnitSize;
		pMyBlock->nFirst = *((USHORT*)pFree);
		pMyBlock->nFree--;

		return (void*)pFree;
	}
	else
	{
		//û���ҵ���˵��ԭ�����ڴ�鶼���ˣ�Ҫ�ٴη���

		if( 0 == nGrowSize)
			return NULL;

		pMyBlock = (MemoryBlock*)new(nUnitSize,nGrowSize) MemoryBlock(nUnitSize,nGrowSize);

		if( NULL == pMyBlock)
			return NULL;

		//����һ�β������
		pMyBlock->pNext = pBlock;
		pBlock = pMyBlock;

		return (void*)pMyBlock->aData;
	}
}

void MemoryPool::Free( void* pFree )
{
	//�ҵ�p���ڵ��ڴ��
	MemoryBlock* pMyBlock = pBlock;
	MemoryBlock* PreBlock = NULL;
	while ( pMyBlock != NULL && ( pBlock->aData > pFree || pFree > pMyBlock->aData + pMyBlock->nSize))
	{
		PreBlock = pMyBlock;
		pMyBlock = pMyBlock->pNext;
	}

	if( NULL != pMyBlock )      //���ڴ��ڱ��ڴ����pMyBlock��ָ����ڴ����
	{      
		//Step1 �޸���������
		*((USHORT*)pFree) = pMyBlock->nFirst;
		pMyBlock->nFirst  = (USHORT)((ULONG)pFree - (ULONG)pMyBlock->aData) / nUnitSize;
		pMyBlock->nFree++;

		//Step2 �ж��Ƿ���Ҫ��OS�ͷ��ڴ�
		if( pMyBlock->nSize == pMyBlock->nFree * nUnitSize )
		{
			//��������ɾ����block

			delete(pMyBlock);
			if(PreBlock)
				PreBlock->pNext = NULL;
			else
				pBlock = NULL; 
		}
		else
		{
			//����block���뵽����
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

		// �����޷�ͳ���ͷţ����������ڴ��һ�㶼��ȫ���Եģ����ԣ��˴���ͳ��Ҳ�ͱ���޹ؽ�Ҫ��

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
