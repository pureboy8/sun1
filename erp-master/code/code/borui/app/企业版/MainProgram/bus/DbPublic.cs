using System;
using System.Collections.Generic;
using System.Text;
using System.Configuration;
using System.Runtime.InteropServices;
using System.Data;
using TIV.Core.DatabaseAccess;
using TIV.Core.TivLogger;
using MainProgram.model;

namespace MainProgram.bus
{
    using DatabaseAccessFactoryInstance = TIV.Core.BaseCoreLib.Singleton<DatabaseFactory>;

    class DbPublic
    {
        private string m_currentLoginUserName = "";
        private int m_currentLoginUserID = 0;
        static private DbPublic m_instance = null;

        private bool m_isGenuineSoftware = false;
        private string m_softwareKey = "";

        private DbPublic()
        {
            m_softwareKey = InitSubSystemSign.getInctance().getRegistersSoftwareKey();
            m_isGenuineSoftware = m_softwareKey.Length == 0 ? false : true;
        }

        static public DbPublic getInctance()
        {
            if (m_instance == null)
            {
                m_instance = new DbPublic();
            }

            return m_instance;
        }

        public int getTableMaxPkey(string tableName)
        {
            int maxid = 0;
            string query = "SELECT MAX(PKEY) FROM " + tableName;

            using (DataTable dataTable = DatabaseAccessFactoryInstance.Instance.QueryDataTable(FormMain.DB_NAME, query))
            {
                if (dataTable.Rows.Count > 0)
                {
                    string temp = DbDataConvert.ToString(dataTable.Rows[0][0]);
                    if (temp.Length > 0)
                    {
                        maxid = Convert.ToInt32(temp.ToString());
                    }
                }
            }

            return maxid; 
        }

        public int tableRecordCount(string sql)
        {
            int count = 0;

            using (DataTable dataTable = DatabaseAccessFactoryInstance.Instance.QueryDataTable(FormMain.DB_NAME, sql))
            {
                count = DbDataConvert.ToInt32(dataTable.Rows[0][0]);
            }

            return count;
        }

        public string getCurrentLoginUserName()
        {
            return m_currentLoginUserName;
        }

        public int getCurrentLoginUserID()
        {
            return m_currentLoginUserID;
        }

        public void setCurrentLoginUserName(string currentLoginUserName)
        {
            m_currentLoginUserName = currentLoginUserName;
        }

        public void setCurrentLoginUserID(int currentLoginUserID)
        {
            m_currentLoginUserID = currentLoginUserID;
        }

        // ��ǰ��ڼ��Ƿ��Ѿ�����
        public bool isCheckOut()
        {
            bool isRet = false;

            string systemDate = DateTime.Now.ToString("yyyyMMdd");
            string year = systemDate.Substring(0, 4);
            string month = systemDate.Substring(4, 2);

            string sql = "SELECT * FROM CASH_BALANCE_LAST_MONTH WHERE YEAR = '";
            sql += year;
            sql += "' AND MONTH = '";
            sql += month;
            sql += "' AND NOTE = '��ת���'";

            using (DataTable dataTable = DatabaseAccessFactoryInstance.Instance.QueryDataTable(FormMain.DB_NAME, sql))
            {
                if (dataTable.Rows.Count > 0)
                {
                    isRet = true;
                }
            }

            return isRet;
        }

        // �õ���ǰ����ڼ�
        public string getCurrentDateStage()
        {
            string str = Convert.ToString(DateTime.Now.Year) + "���" + Convert.ToString(DateTime.Now.Month) + "��";
            return str;
        }

        // ����Ƿ��Ѿ�ע��Ϊ����
        public bool isGenuineSoftware()
        {
            return m_isGenuineSoftware;
        }

        // ����Ƿ��Ѿ�ע��Ϊ����
        public string getRegisterSoftwareKey()
        {
            return m_softwareKey;
        }
    }
}