#include <cstdio>

template <typename T> class Singleton_2B
{
protected:
	typedef  T  object_type;
	//���õ�����ľ�̬ȫ�ֱ���
	static T instance_;
public:
	static T* instance()
	{
		return &instance_;
	}
};

//��Ϊ����ľ�̬������������һ��ͨ�õ�����
template<typename T> typename Singleton_2B<T>::object_type  Singleton_2B<T>::instance_;

//���Ե����Ӵ��롣
class Object_2B_1
{

	//��ʵʹ����Ԫ�������ǿ�����Object_2B�Ĺ��캯����protected�ģ��Ӷ�����ʵ�ֵ��ӵ���ͼ
	friend class Singleton_2B<Object_2B_1>;
	//ע��������protected������޷�����ʵ��
protected:
	Object_2B_1();
	~Object_2B_1(){};
public:
	void do_something();
protected:
	int data_2b_1_;
};

class Object_2B_2
{
	friend class Singleton_2B<Object_2B_2>;
protected:
	Object_2B_2();
	~Object_2B_2(){};
public:
	void do_something();
protected:
	int data_2b_2_;
};

//CPP�ļ�
Object_2B_1::Object_2B_1():
	data_2b_1_(1)
{
	printf("Object_2B_1::Object_2B_1() this:[%p] data_2b_1_ [%d].\n",this,data_2b_1_);
	Singleton_2B<Object_2B_2>::instance()->do_something();    
};

void Object_2B_1::do_something()
{
	data_2b_1_+= 10000;
	printf("Object_2B_1::do_something() this:[%p] data_2b_1_ [%d].\n",this,data_2b_1_);

}


Object_2B_2::Object_2B_2():
	data_2b_2_(2)
{
	printf("Object_2B_2::Object_2B_2() this:[%p] data_2b_2_ [%d].\n",this,data_2b_2_);
	Singleton_2B<Object_2B_1>::instance()->do_something();
};

void Object_2B_2::do_something()
{
	data_2b_2_+= 10000;
	printf("Object_2B_2::do_something() this:[%p] data_2b_2_ [%d].\n",this,data_2b_2_);
}

