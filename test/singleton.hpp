#include <cstdio>

template <typename T> class Singleton_2B
{
protected:
	typedef  T  object_type;
	//利用的是类的静态全局变量
	static T instance_;
public:
	static T* instance()
	{
		return &instance_;
	}
};

//因为是类的静态变量，必须有一个通用的声明
template<typename T> typename Singleton_2B<T>::object_type  Singleton_2B<T>::instance_;

//测试的例子代码。
class Object_2B_1
{

	//其实使用友元帮助我们可以让Object_2B的构造函数是protected的，从而真正实现单子的意图
	friend class Singleton_2B<Object_2B_1>;
	//注意下面用protected，大家无法构造实例
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

//CPP文件
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

