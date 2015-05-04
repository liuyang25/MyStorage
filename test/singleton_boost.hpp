#include <cstdio>

template <typename T>
class Singleton_WY
{
private:
	struct object_creator
	{
		object_creator() 
		{
			Singleton_WY<T>::instance(); 
		}
		inline void do_nothing() const {}
	};
	//利用类的静态对象object_creator的构造初始化,在进入main之前已经调用了instance
	//从而避免了多次初始化的问题
	static object_creator create_object_;
public:
	static T *instance()
	{
		static T obj;
		//do_nothing 是必要的，do_nothing的作用有点意思，
		//如果不加create_object_.do_nothing();这句话，在main函数前面
		//create_object_的构造函数都不会被调用，instance当然也不会被调用，
		//我的估计是模版的延迟实现的特效导致，如果没有这句话，编译器也不会实现
		// Singleton_WY<T>::object_creator,所以就会导致这个问题
		create_object_.do_nothing();
		return &obj;
	}
};
//因为create_object_是类的静态变量，必须有一个通用的声明
template <typename T>  typename Singleton_WY<T>::object_creator Singleton_WY<T>::create_object_;

//测试的例子
class Object_WY_1
{
	//其实使用友元帮助我们可以让Object_2B的构造函数是protected的，从而真正实现单子的意图
	friend class Singleton_WY<Object_WY_1>;
	//注意下面用protected，大家无法构造实例
protected:
	Object_WY_1();
	~Object_WY_1(){};
public:
	void do_something();
protected:
	int data_wy_1_;
};

class Object_WY_2
{
	friend class Singleton_WY<Object_WY_2>;
protected:
	Object_WY_2();
	~Object_WY_2(){};
public:
	void do_something();
protected:
	int data_wy_2_;
};

//CPP代码
Object_WY_1::Object_WY_1():
	data_wy_1_(1)
{
	printf("Object_WY_1::Object_WY_1() this:[%p] data_2b_1_ [%d].\n",this,data_wy_1_);
	Singleton_WY<Object_WY_2>::instance()->do_something();    
};

void Object_WY_1::do_something()
{
	data_wy_1_+= 10000;
	printf("Object_2B_1::do_something() this:[%p] data_2b_1_ [%d].\n",this,data_wy_1_);

}


Object_WY_2::Object_WY_2():
	data_wy_2_(2)
{
	printf("Object_WY_2::Object_WY_2() this:[%p] data_2b_2_ [%d].\n",this,data_wy_2_);
	Singleton_WY<Object_WY_1>::instance()->do_something();
};

void Object_WY_2::do_something()
{
	data_wy_2_+= 10000;
	printf("Object_WY_2::do_something() this:[%p] data_2b_2_ [%d].\n",this,data_wy_2_);
}
