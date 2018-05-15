﻿using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;
using TIV.Core.DatabaseAccess;
using TIV.Core.TivLogger;

namespace DutyManager
{
    using DatabaseAccessFactoryInstance = TIV.Core.BaseCoreLib.Singleton<DatabaseFactory>;

    public partial class FormLogin : Form
    {
        private bool m_loginSuccessful = false;
        public static string m_currentUserStaffName = "";
        public static string m_currentLoginUserID = "";
        public static string m_currentLoginUserName = "";
        public static string m_currentLoginPassword = "";
        public static string TCC_TRAIN_DM_DATABASE = "Tcctraindm";

        public FormLogin()
        {
            InitializeComponent();
        }

        private void FormLogin_Load(object sender, EventArgs e)
        {
        }

        private void buttonEnter_Click(object sender, EventArgs e)
        {
            string userName = this.textBoxUserName.Text.ToString();
            string password = this.textBoxPassword.Text.ToString();

            string query = "SELECT ID, STAFF_NAME, USER_NAME, PASSWORD FROM DUTY_STAFF_LIST WHERE USER_NAME = '";
            query += userName;
            query += "'";

            // 初始化专业下拉列表框
            try
            {
                using (DataTable dataTable = DatabaseAccessFactoryInstance.Instance.QueryDataTable(FormLogin.TCC_TRAIN_DM_DATABASE, query))
                {
                    if (dataTable.Rows.Count > 0)
                    {
                        m_currentLoginUserID = DbDataConvert.ToString(dataTable.Rows[0]["ID"]);
                        m_currentUserStaffName = DbDataConvert.ToString(dataTable.Rows[0]["STAFF_NAME"]);
                        m_currentLoginUserName = DbDataConvert.ToString(dataTable.Rows[0]["USER_NAME"]);
                        m_currentLoginPassword = DbDataConvert.ToString(dataTable.Rows[0]["PASSWORD"]);
                    }
                }

                if (m_currentLoginUserID.Length == 0)
                {
                    this.textBoxUserName.Text = "";
                    this.textBoxPassword.Text = "";

                    MessageBoxExtend.messageWarning("用户名不存在，请重新输入！");

                    return;
                }
                else 
                {
                    if (m_currentLoginUserName.CompareTo("system") != 0)
                    {
                        MessageBoxExtend.messageWarning("只有[system]才能登陆该系统，请使用system账户重新登录！");
                        this.textBoxUserName.Text = "";
                        this.textBoxPassword.Text = "";
                        return;
                    }
                }

                if (m_currentLoginPassword.CompareTo(password) != 0)
                {
                    MessageBox.Show("密码错误，请重新输入！", "警告 ", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                    this.textBoxPassword.Text = "";
                    return;
                }
                else 
                {
                    // 此处代表用户登录成功
                    m_loginSuccessful = true;
                    this.Close();
                }
            }
            catch (Exception error)
            {
                MessageBox.Show(error.Message, "警告 ", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                return;
            }
        }

        public bool loginSuccessful()
        {
            return m_loginSuccessful;
        }
    }
}

IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[WAREHOUSE_MANAGEMENT_PRO_OCCUPIED]') AND type in (N'U'))
DROP TABLE [dbo].[WAREHOUSE_MANAGEMENT_PRO_OCCUPIED]
CREATE TABLE [dbo].[WAREHOUSE_MANAGEMENT_PRO_OCCUPIED](
	[PKEY] [int] IDENTITY(1,1) NOT NULL,
	[TRADING_DATE] [datetime] NOT NULL,
	[BILL_NUMBER] [nvarchar](20) COLLATE Chinese_PRC_CI_AS NOT NULL,
	[EXCHANGES_UNIT] [nvarchar](100) COLLATE Chinese_PRC_CI_AS NULL,
	[SUM_VALUE] [int] NOT NULL,
	[SUM_MONEY] [money] NOT NULL,
	[MAKE_ORDER_STAFF] [int] NOT NULL,
	[APPLY_STAFF] [int] NOT NULL,
	[ORDERR_REVIEW] [int] NULL,
	[REVIEW_DATE] [datetime] NULL,
	[IS_REVIEW] [int] NULL,
	[IS_CANCEL] [int] NULL
) ON [PRIMARY];

----2016-06-04 增加预占库存功能，增加预占库存清单表(WAREHOUSE_MANAGEMENT_PRO_OCCUPIED_DETAILS)
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[WAREHOUSE_MANAGEMENT_PRO_OCCUPIED_DETAILS]') AND type in (N'U'))
DROP TABLE [dbo].[WAREHOUSE_MANAGEMENT_PRO_OCCUPIED_DETAILS]
CREATE TABLE [dbo].[WAREHOUSE_MANAGEMENT_PRO_OCCUPIED_DETAILS](
	[PKEY] [int] IDENTITY(1,1) NOT NULL,
	[ROW_NUMBER] [int] NOT NULL,
	[MATERIEL_ID] [int] NOT NULL,
	[BILL_NUMBER] [nvarchar](20) COLLATE Chinese_PRC_CI_AS NOT NULL,
	[PRICE] [money] NOT NULL,
	[VALUE] [int] NOT NULL,
	[NOTE] [nvarchar](200) COLLATE Chinese_PRC_CI_AS NULL
) ON [PRIMARY];