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
	//������ľ�̬����object_creator�Ĺ����ʼ��,�ڽ���main֮ǰ�Ѿ�������instance
	//�Ӷ������˶�γ�ʼ��������
	static object_creator create_object_;
public:
	static T *instance()
	{
		static T obj;
		//do_nothing �Ǳ�Ҫ�ģ�do_nothing�������е���˼��
		//�������create_object_.do_nothing();��仰����main����ǰ��
		//create_object_�Ĺ��캯�������ᱻ���ã�instance��ȻҲ���ᱻ���ã�
		//�ҵĹ�����ģ����ӳ�ʵ�ֵ���Ч���£����û����仰��������Ҳ����ʵ��
		// Singleton_WY<T>::object_creator,���Ծͻᵼ���������
		create_object_.do_nothing();
		return &obj;
	}
};
//��Ϊcreate_object_����ľ�̬������������һ��ͨ�õ�����
template <typename T>  typename Singleton_WY<T>::object_creator Singleton_WY<T>::create_object_;

//���Ե�����
class Object_WY_1
{
	//��ʵʹ����Ԫ�������ǿ�����Object_2B�Ĺ��캯����protected�ģ��Ӷ�����ʵ�ֵ��ӵ���ͼ
	friend class Singleton_WY<Object_WY_1>;
	//ע��������protected������޷�����ʵ��
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

//CPP����
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
