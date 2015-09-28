#include <iostream>
#include <boost/program_options.hpp>
#include <boost/date_time.hpp>
#include <fstream>
#include <boost/property_tree/xml_parser.hpp>
using namespace std;

void test_date()
{
    using namespace boost;
    gregorian::date dt = gregorian::day_clock::local_day();
    cout<<"iso:"<<gregorian::to_iso_string(dt)<<endl;
    cout<<"iso-extended:"<<gregorian::to_iso_extended_string(dt)<<endl;
    cout<<"simple:"<<gregorian::to_simple_string(dt)<<endl;
    cout<<"sql:"<<gregorian::to_sql_string(dt)<<endl;
    //gregorian::date dt = gregorian::day_clock::local_day_ymd();
}
void test_time()
{
    using namespace boost;
    posix_time::ptime pt = posix_time::second_clock::local_time();
    cout<<"iso:"<<posix_time::to_iso_string(pt)<<endl;
    cout<<"iso-extended:"<<posix_time::to_iso_extended_string(pt)<<endl;
    cout<<"simple:"<<posix_time::to_simple_string(pt)<<endl;
}

template<typename T>
T foo()
{
    T t;
    return t;
}

template<typename T>
T foo_test()
{
    return foo<T>();
}

void test_template()
{
    cout<<foo_test<int>()<<endl;
}

void test_xml()
{
    fstream fin;
    fin.open("123.xml",ios_base::in);
    if(fin.is_open())
    {
        boost::property_tree::ptree pt;
        boost::property_tree::read_xml(fin,pt);
//        pt = pt.get_child("config.books.name");
//        string name = pt.get_value<string>("888");
//        cout<<name<<endl;
        //string name = pt.get<string>("config.books.name");

        for(auto pa:pt.get_child("config"))
        {
            string txt = pa.first;
            boost::property_tree::ptree p1 = pa.second;
            boost::property_tree::ptree pBook = p1.get_child("name");
            string name = pBook.get_value<string>("==");
            cout<<txt<<":"<<name<<endl;
        }
    }
    else
    {
        cout<<"file not found"<<endl;
    }
    fin.close();
}

#include <boost/unordered_map.hpp>
#include <boost/unordered_set.hpp>
void test_hash()
{
    using namespace boost;
}

void test_basic()
{
    double db = 9.999;
    long l = db;
    cout<<"556778\\bkkk:"<<endl;
    cout<<"556778\bkkk"<<endl;
    cout<<db<<"\t"<<l<<endl;
    l = reinterpret_cast<long&>(db);
    cout<<db<<"\t"<<l<<endl;
}
int main(int argc,char * argv[])
{
    using namespace boost::program_options;
    options_description desc("Allowed options");
    desc.add_options()
            ("help,h","help option")
            //("choose,c",value<int>(),"choose test no.")
            ("date","date test")
            ("time","time test")
            ("xml","xml test")
            ("template","template test")
            ("hash","hash test")
            ("basic","basic test")
            ;
    variables_map vm;
    try
    {
        store(parse_command_line(argc,argv,desc),vm);
    }
    catch(boost::program_options::error &e)
    {
        cout<<e.what()<<endl;
        return 0;
    }

    if(vm.count("help"))
    {
        cout<<desc<<endl;
    }
    else if(vm.count("date"))
    {
        test_date();
    }
    else if(vm.count("time"))
    {
        test_time();
    }
    else if(vm.count("xml"))
    {
        test_xml();
    }
    else if(vm.count("template"))
    {
        test_template();
    }
    else if(vm.count("hash"))
    {
        test_hash();
    }
    else if("basic")
    {
        test_basic();
    }
    else
    {
        cout<<"error"<<endl;
    }

    return 0;
}

