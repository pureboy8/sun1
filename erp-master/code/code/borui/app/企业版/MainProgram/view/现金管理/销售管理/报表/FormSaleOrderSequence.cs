﻿using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;
using System.Collections;
using MainProgram.model;
using MainProgram.bus;

namespace MainProgram
{
    public partial class FormSaleOrderSequence : Form
    {
        public enum OrderType
        {
            // 销售管理-销售报价单时序簿
            SaleQuotation,

            // 销售管理-销售订单时序簿
            SaleOrder,

            // 销售管理-销售出库单时序簿
            SaleOut,

            // 销售管理-销售发票时序簿
            SaleInvoice,

            // 销售管理-销售订单执行情况
            SaleOrderExcute,

            // 销售管理-销售出库单收款情况
            SaleOutOrderExcute,

            // 仓存管理-生产领料
            StorageMaterielOut,

            // 仓存管理-盘亏亏损
            StorageOutCheck,

            // 仓存管理-其他出库
            StorageOutOther
        };

        private int m_dataGridRecordCount = 0;
        private OrderType m_orderType;
        private string m_billNumber = "";
        private bool m_isSelectOrderNumber;

        private DataGridViewExtend m_dateGridViewExtend = new DataGridViewExtend();
        private FormStorageSequenceFilterValue m_filter = new FormStorageSequenceFilterValue();

        public FormSaleOrderSequence(OrderType orderType, bool isSelectOrderNumber = false)
        {
            InitializeComponent();

            m_orderType = orderType;
            m_isSelectOrderNumber = isSelectOrderNumber;

            this.Text = getWindowText(OrderType.SaleOrder);
        }

        private void FormSaleOrderSequence_Load(object sender, EventArgs e)
        {
            if (m_orderType == OrderType.SaleOrder)
            {
                m_dateGridViewExtend.addDataGridViewColumn("ID", 30);
                m_dateGridViewExtend.addDataGridViewColumn("客户", 150);
                m_dateGridViewExtend.addDataGridViewColumn("交易日期", 100);
                m_dateGridViewExtend.addDataGridViewColumn("单据号", 120);
                m_dateGridViewExtend.addDataGridViewColumn("交易类型", 120);
                m_dateGridViewExtend.addDataGridViewColumn("约定供货日期", 160);
                m_dateGridViewExtend.addDataGridViewColumn("约定付款日期", 160);
                m_dateGridViewExtend.addDataGridViewColumn("金额合计", 100);
                m_dateGridViewExtend.addDataGridViewColumn("运输费用合计", 160);
                m_dateGridViewExtend.addDataGridViewColumn("其他费用合计", 160);
                m_dateGridViewExtend.addDataGridViewColumn("总金额", 100);
                m_dateGridViewExtend.addDataGridViewColumn("业务员", 100);
                m_dateGridViewExtend.addDataGridViewColumn("制单员", 100);
                m_dateGridViewExtend.addDataGridViewColumn("是否审核", 100);
                m_dateGridViewExtend.addDataGridViewColumn("审核员", 100);
                m_dateGridViewExtend.addDataGridViewColumn("审核日期", 100);
            }
            else if (m_orderType == OrderType.SaleOut)
            {
                m_dateGridViewExtend.addDataGridViewColumn("ID", 30);
                m_dateGridViewExtend.addDataGridViewColumn("客户", 150);
                m_dateGridViewExtend.addDataGridViewColumn("交易日期", 100);
                m_dateGridViewExtend.addDataGridViewColumn("单据号", 120);
                m_dateGridViewExtend.addDataGridViewColumn("交易类型", 120);
                m_dateGridViewExtend.addDataGridViewColumn("约定付款日期", 160);
                m_dateGridViewExtend.addDataGridViewColumn("源单据号", 150);
                m_dateGridViewExtend.addDataGridViewColumn("金额合计", 100);
                m_dateGridViewExtend.addDataGridViewColumn("运输费用合计", 160);
                m_dateGridViewExtend.addDataGridViewColumn("其他费用合计", 160);
                m_dateGridViewExtend.addDataGridViewColumn("总金额", 100);
                m_dateGridViewExtend.addDataGridViewColumn("保管员", 100);
                m_dateGridViewExtend.addDataGridViewColumn("验收员", 100);
                m_dateGridViewExtend.addDataGridViewColumn("业务员", 100);
                m_dateGridViewExtend.addDataGridViewColumn("制单员", 100);
                m_dateGridViewExtend.addDataGridViewColumn("审核员", 100);
                m_dateGridViewExtend.addDataGridViewColumn("审核日期", 100);
                m_dateGridViewExtend.addDataGridViewColumn("记账", 100);
                m_dateGridViewExtend.addDataGridViewColumn("记账日期", 100);
            }
            else if (m_orderType == OrderType.SaleInvoice)
            {
                MessageBoxExtend.messageWarning("暂时不支持销售发票序时薄类型");
            }
            else if (m_orderType == OrderType.SaleOrderExcute)
            {
                m_dateGridViewExtend.addDataGridViewColumn("ID", 30);
                m_dateGridViewExtend.addDataGridViewColumn("客户", 150);
                m_dateGridViewExtend.addDataGridViewColumn("交易日期", 100);
                m_dateGridViewExtend.addDataGridViewColumn("单据号", 120);
                m_dateGridViewExtend.addDataGridViewColumn("约定供货日期", 150);
                m_dateGridViewExtend.addDataGridViewColumn("订单物料总数量", 150);
                m_dateGridViewExtend.addDataGridViewColumn("是否已出库", 150);
                m_dateGridViewExtend.addDataGridViewColumn("实际出库数量", 150);
                m_dateGridViewExtend.addDataGridViewColumn("业务员", 100);
            }
            else if (m_orderType == OrderType.SaleOutOrderExcute)
            {
                m_dateGridViewExtend.addDataGridViewColumn("ID", 30);
                m_dateGridViewExtend.addDataGridViewColumn("客户", 150);
                m_dateGridViewExtend.addDataGridViewColumn("交易日期", 100);
                m_dateGridViewExtend.addDataGridViewColumn("单据号", 120);
                m_dateGridViewExtend.addDataGridViewColumn("销售类型", 100);
                m_dateGridViewExtend.addDataGridViewColumn("约定付款日期", 110);
                m_dateGridViewExtend.addDataGridViewColumn("费用总金额", 100);
                m_dateGridViewExtend.addDataGridViewColumn("已收款金额", 100);
                m_dateGridViewExtend.addDataGridViewColumn("未收款金额", 100);
                m_dateGridViewExtend.addDataGridViewColumn("业务员", 100);
            }
            else if (m_orderType == OrderType.SaleQuotation)
            {
                m_dateGridViewExtend.addDataGridViewColumn("ID", 30);
                m_dateGridViewExtend.addDataGridViewColumn("客户名称", 140);
                m_dateGridViewExtend.addDataGridViewColumn("日期", 80);
                m_dateGridViewExtend.addDataGridViewColumn("单据号", 120);
                m_dateGridViewExtend.addDataGridViewColumn("报价及跟踪信息", 250);
                m_dateGridViewExtend.addDataGridViewColumn("备注", 100);
                m_dateGridViewExtend.addDataGridViewColumn("业务员", 80);
                m_dateGridViewExtend.addDataGridViewColumn("联系人", 80);
                m_dateGridViewExtend.addDataGridViewColumn("联系电话", 80);
            }
            else if (m_orderType == OrderType.StorageMaterielOut)
            {
                // 生产领料单序时薄
                m_dateGridViewExtend.addDataGridViewColumn("ID", 30);
                m_dateGridViewExtend.addDataGridViewColumn("领料部门", 140);
                m_dateGridViewExtend.addDataGridViewColumn("日期", 80);
                m_dateGridViewExtend.addDataGridViewColumn("单据号", 120);
                m_dateGridViewExtend.addDataGridViewColumn("数量", 80);
                m_dateGridViewExtend.addDataGridViewColumn("金额", 80);
                m_dateGridViewExtend.addDataGridViewColumn("领料人", 80);
                m_dateGridViewExtend.addDataGridViewColumn("制单人", 80);
                m_dateGridViewExtend.addDataGridViewColumn("审核人", 80);
                m_dateGridViewExtend.addDataGridViewColumn("审核日期", 80);
            }
            else if (m_orderType == OrderType.StorageOutCheck)
            {
                // 盘亏毁损单序时薄
                m_dateGridViewExtend.addDataGridViewColumn("ID", 30);
                m_dateGridViewExtend.addDataGridViewColumn("领料部门", 140, false);
                m_dateGridViewExtend.addDataGridViewColumn("日期", 80);
                m_dateGridViewExtend.addDataGridViewColumn("单据号", 120);
                m_dateGridViewExtend.addDataGridViewColumn("数量", 80);
                m_dateGridViewExtend.addDataGridViewColumn("金额", 80);
                m_dateGridViewExtend.addDataGridViewColumn("领料人", 80);
                m_dateGridViewExtend.addDataGridViewColumn("制单人", 80);
                m_dateGridViewExtend.addDataGridViewColumn("审核人", 80);
                m_dateGridViewExtend.addDataGridViewColumn("审核日期", 80);
            }
            else if (m_orderType == OrderType.StorageOutOther)
            {
                // 其他出库单序时薄
                m_dateGridViewExtend.addDataGridViewColumn("ID", 30);
                m_dateGridViewExtend.addDataGridViewColumn("领料部门", 140, false);
                m_dateGridViewExtend.addDataGridViewColumn("日期", 80);
                m_dateGridViewExtend.addDataGridViewColumn("单据号", 120);
                m_dateGridViewExtend.addDataGridViewColumn("数量", 80);
                m_dateGridViewExtend.addDataGridViewColumn("金额", 80);
                m_dateGridViewExtend.addDataGridViewColumn("领料人", 80);
                m_dateGridViewExtend.addDataGridViewColumn("制单人", 80);
                m_dateGridViewExtend.addDataGridViewColumn("审核人", 80);
                m_dateGridViewExtend.addDataGridViewColumn("审核日期", 80);
            }
            else
            {
                MessageBoxExtend.messageWarning("暂时不支持的序时薄类型");
            }

            m_dateGridViewExtend.initDataGridViewColumn(this.dataGridViewList);
            updateDataGridView();
        }

        private void updateDataGridView()
        {
            SortedDictionary<int, ArrayList> sortedDictionaryList = new SortedDictionary<int, ArrayList>();

            if (m_orderType == OrderType.SaleOrder)
            {
                SortedDictionary<int, SaleOrderTable> list = new SortedDictionary<int, SaleOrderTable>();
                list = SaleOrder.getInctance().getAllSaleOrderInfo();

                m_dataGridRecordCount = list.Count;

                for (int index = 0; index < list.Count; index++)
                {
                    SaleOrderTable record = new SaleOrderTable();
                    record = (SaleOrderTable)list[index];

                    ArrayList temp = new ArrayList();

                    temp.Add(record.pkey);
                    temp.Add(record.customerName);
                    temp.Add(record.tradingDate);
                    temp.Add(record.billNumber);
                    temp.Add(record.saleType);
                    temp.Add(record.deliveryDate);
                    temp.Add(record.paymentDate);
                    temp.Add(record.sumMoney);
                    temp.Add(record.sumTransportationCost);
                    temp.Add(record.sumOtherCost);
                    temp.Add(record.totalMoney);
                    temp.Add(record.businessPeopleName);
                    temp.Add(record.makeOrderStaffName);

                    if (record.isReview == "0")
                    {
                        temp.Add("否");
                    }
                    else
                    {
                        temp.Add("是");
                    }

                    temp.Add(record.orderrReviewName);
                    temp.Add(record.reviewDate);

                    sortedDictionaryList.Add(index, temp);
                }

                m_dateGridViewExtend.initDataGridViewData(sortedDictionaryList, 3);
            }
            else if (m_orderType == OrderType.SaleOut)
            {
                SortedDictionary<int, SaleOutOrderTable> list = new SortedDictionary<int, SaleOutOrderTable>();
                list = SaleOutOrder.getInctance().getAllSaleOutOrderInfo();

                m_dataGridRecordCount = list.Count;

                for (int index = 0; index < list.Count; index++)
                {
                    SaleOutOrderTable record = new SaleOutOrderTable();
                    record = (SaleOutOrderTable)list[index];

                    ArrayList temp = new ArrayList();

                    temp.Add(record.pkey);
                    temp.Add(record.customerName);
                    temp.Add(record.tradingDate);
                    temp.Add(record.billNumber);
                    temp.Add(record.saleType);
                    temp.Add(record.paymentDate);
                    temp.Add(record.sourceBillNumber);
                    temp.Add(record.sumMoney);
                    temp.Add(record.sumTransportationCost);
                    temp.Add(record.sumOtherCost);
                    temp.Add(record.totalMoney);
                    temp.Add(record.staffSaveName);
                    temp.Add(record.staffCheckName);
                    temp.Add(record.businessPeopleName);
                    temp.Add(record.makeOrderStaffName);
                    temp.Add(record.orderrReviewName);
                    temp.Add(record.reviewDate);
                    temp.Add(record.orderInLedgerName);
                    temp.Add(record.inLedgerDate);

                    sortedDictionaryList.Add(index, temp);
                }

                m_dateGridViewExtend.initDataGridViewData(sortedDictionaryList, 3);
            }
            else if (m_orderType == OrderType.SaleInvoice)
            {
            }
            else if (m_orderType == OrderType.SaleOrderExcute)
            {
                SortedDictionary<int, SaleOrderTable> list = new SortedDictionary<int, SaleOrderTable>();
                list = SaleOrder.getInctance().getAllSaleOrderInfo();

                m_dataGridRecordCount = list.Count;

                for (int index = 0; index < list.Count; index++)
                {
                    SaleOrderTable record = new SaleOrderTable();
                    record = (SaleOrderTable)list[index];

                    ArrayList temp = new ArrayList();

                    temp.Add(record.pkey);
                    temp.Add(record.customerName);
                    temp.Add(record.tradingDate);
                    temp.Add(record.billNumber);
                    temp.Add(record.deliveryDate);
                    temp.Add(record.sumValue);

                    if (record.isInStorage == "0")
                    {
                        temp.Add("否");
                    }
                    else
                    {
                        temp.Add("是");
                    }

                    temp.Add(record.actualValue);
                    temp.Add(record.businessPeopleName);

                    sortedDictionaryList.Add(index, temp);
                }

                m_dateGridViewExtend.initDataGridViewData(sortedDictionaryList, 3);
            }
            else if (m_orderType == OrderType.SaleOutOrderExcute)
            {
                SortedDictionary<int, SaleOutOrderTable> list = new SortedDictionary<int, SaleOutOrderTable>();
                list = SaleOutOrder.getInctance().getAllSaleOutOrderInfo();

                m_dataGridRecordCount = list.Count;

                for (int index = 0; index < list.Count; index++)
                {
                    SaleOutOrderTable record = new SaleOutOrderTable();
                    record = (SaleOutOrderTable)list[index];

                    ArrayList temp = new ArrayList();

                    temp.Add(record.pkey);
                    temp.Add(record.customerName);
                    temp.Add(record.tradingDate);
                    temp.Add(record.billNumber);
                    temp.Add(record.saleType);
                    temp.Add(record.paymentDate);
                    temp.Add(record.totalMoney);
                    temp.Add(record.paymentOk);
                    temp.Add(record.paymentNoOk);
                    temp.Add(record.businessPeopleName);

                    sortedDictionaryList.Add(index, temp);
                }

                m_dateGridViewExtend.initDataGridViewData(sortedDictionaryList, 3);
            }
            else if (m_orderType == OrderType.SaleQuotation)
            {
                SortedDictionary<int, SaleQuotationOrderTable> list = new SortedDictionary<int, SaleQuotationOrderTable>();
                list = SaleQuotationOrder.getInctance().getAllSaleQuotationOrderInfo();

                m_dataGridRecordCount = list.Count;

                for (int index = 0; index < list.Count; index++)
                {
                    SaleQuotationOrderTable record = new SaleQuotationOrderTable();
                    record = (SaleQuotationOrderTable)list[index];

                    ArrayList temp = new ArrayList();

                    temp.Add(record.pkey);
                    temp.Add(record.customerName);
                    temp.Add(record.date);
                    temp.Add(record.billNumber);
                    temp.Add(record.content);
                    temp.Add(record.note);
                    temp.Add(record.salemanName);
                    temp.Add(record.contact);
                    temp.Add(record.tel);

                    sortedDictionaryList.Add(index, temp);
                }

                m_dateGridViewExtend.initDataGridViewData(sortedDictionaryList, 3);
            }
            else if (m_orderType == OrderType.StorageMaterielOut)
            {
                // 生产领料单序时薄
                SortedDictionary<int, MaterielOutOrderTable> list = new SortedDictionary<int, MaterielOutOrderTable>();
                list = MaterielOutOrder.getInctance().getAllMaterielOutOrderInfo();

                m_dataGridRecordCount = list.Count;

                for (int index = 0; index < list.Count; index++)
                {
                    bool isDisplayRecord = false;
                    MaterielOutOrderTable record = new MaterielOutOrderTable();
                    record = (MaterielOutOrderTable)list[index];

                    if (record.tradingDate.CompareTo(m_filter.startDate) >=0 && record.tradingDate.CompareTo(m_filter.endDate) <= 0)
                    {
                        // 等于0代表只显示已审核单据
                        if (m_filter.allReview == "0")
                        {
                            if (record.isReview == "1")
                            {
                                if (m_filter.billColor == "0")  // 需要显示蓝字单据
                                {
                                    if (record.isRedBill == 0)
                                    {
                                        isDisplayRecord = true;
                                    }
                                }
                                else if (m_filter.billColor == "1")  // 需要显示红字单据
                                {
                                    if (record.isRedBill == 1)
                                    {
                                        isDisplayRecord = true;
                                    }
                                }
                                else                                // 需要显示全部颜色单据
                                {
                                    isDisplayRecord = true;
                                }
                            }
                        }
                        else
                        {
                            if (m_filter.billColor == "0")  // 需要显示蓝字单据
                            {
                                if (record.isRedBill == 0)
                                {
                                    isDisplayRecord = true;
                                }
                            }
                            else if (m_filter.billColor == "1")  // 需要显示红字单据
                            {
                                if (record.isRedBill == 1)
                                {
                                    isDisplayRecord = true;
                                }
                            }
                            else                                // 需要显示全部颜色单据
                            {
                                isDisplayRecord = true;
                            }
                        }
                    }

                    if (isDisplayRecord)
                    {
                        ArrayList temp = new ArrayList();

                        temp.Add(record.pkey);
                        temp.Add(record.departmentName);
                        temp.Add(record.tradingDate);
                        temp.Add(record.billNumber);
                        temp.Add(record.sumValue);
                        temp.Add(record.sumMoney);
                        temp.Add(record.materielOutStaffName);
                        temp.Add(record.makeOrderStaffName);
                        temp.Add(record.orderrReviewName);
                        temp.Add(record.reviewDate);

                        sortedDictionaryList.Add(index, temp);
                    }
                }

                m_dateGridViewExtend.initDataGridViewData(sortedDictionaryList, 3);
            }
            else if (m_orderType == OrderType.StorageOutCheck)
            {
                // 盘亏毁损单序时薄
                SortedDictionary<int, MaterielOutEarningsOrderTable> list = new SortedDictionary<int, MaterielOutEarningsOrderTable>();
                list = MaterielOutEarningsOrder.getInctance().getAllMaterielOutEarningsOrderInfo();

                m_dataGridRecordCount = list.Count;

                for (int index = 0; index < list.Count; index++)
                {
                    bool isDisplayRecord = false;
                    MaterielOutEarningsOrderTable record = new MaterielOutEarningsOrderTable();
                    record = (MaterielOutEarningsOrderTable)list[index];

                    if (record.tradingDate.CompareTo(m_filter.startDate) >= 0 && record.tradingDate.CompareTo(m_filter.endDate) <= 0)
                    {
                        // 等于0代表只显示已审核单据
                        if (m_filter.allReview == "0")
                        {
                            if (record.isReview == "1")
                            {
                                if (m_filter.billColor == "0")  // 需要显示蓝字单据
                                {
                                    if (record.isRedBill == 0)
                                    {
                                        isDisplayRecord = true;
                                    }
                                }
                                else if (m_filter.billColor == "1")  // 需要显示红字单据
                                {
                                    if (record.isRedBill == 1)
                                    {
                                        isDisplayRecord = true;
                                    }
                                }
                                else                                // 需要显示全部颜色单据
                                {
                                    isDisplayRecord = true;
                                }
                            }
                        }
                        else
                        {
                            if (m_filter.billColor == "0")  // 需要显示蓝字单据
                            {
                                if (record.isRedBill == 0)
                                {
                                    isDisplayRecord = true;
                                }
                            }
                            else if (m_filter.billColor == "1")  // 需要显示红字单据
                            {
                                if (record.isRedBill == 1)
                                {
                                    isDisplayRecord = true;
                                }
                            }
                            else                                // 需要显示全部颜色单据
                            {
                                isDisplayRecord = true;
                            }
                        }
                    }

                    if (isDisplayRecord)
                    {
                        ArrayList temp = new ArrayList();

                        temp.Add(record.pkey);
                        temp.Add("");
                        temp.Add(record.tradingDate);
                        temp.Add(record.billNumber);
                        temp.Add(record.sumValue);
                        temp.Add(record.sumMoney);
                        temp.Add(record.materielOutStaffName);
                        temp.Add(record.makeOrderStaffName);
                        temp.Add(record.orderrReviewName);
                        temp.Add(record.reviewDate);

                        sortedDictionaryList.Add(index, temp);
                    }
                }

                m_dateGridViewExtend.initDataGridViewData(sortedDictionaryList, 3);
            }
            else if (m_orderType == OrderType.StorageOutOther)
            {
                // 其他出库单序时薄
                SortedDictionary<int, MaterielOutOtherOrderTable> list = new SortedDictionary<int, MaterielOutOtherOrderTable>();
                list = MaterielOutOtherOrder.getInctance().getAllMaterielOutOtherOrderInfo();

                m_dataGridRecordCount = list.Count;

                for (int index = 0; index < list.Count; index++)
                {
                    bool isDisplayRecord = false;
                    MaterielOutOtherOrderTable record = new MaterielOutOtherOrderTable();
                    record = (MaterielOutOtherOrderTable)list[index];

                    if (record.tradingDate.CompareTo(m_filter.startDate) >= 0 && record.tradingDate.CompareTo(m_filter.endDate) <= 0)
                    {
                        // 等于0代表只显示已审核单据
                        if (m_filter.allReview == "0")
                        {
                            if (record.isReview == "1")
                            {
                                if (m_filter.billColor == "0")  // 需要显示蓝字单据
                                {
                                    if (record.isRedBill == 0)
                                    {
                                        isDisplayRecord = true;
                                    }
                                }
                                else if (m_filter.billColor == "1")  // 需要显示红字单据
                                {
                                    if (record.isRedBill == 1)
                                    {
                                        isDisplayRecord = true;
                                    }
                                }
                                else                                // 需要显示全部颜色单据
                                {
                                    isDisplayRecord = true;
                                }
                            }
                        }
                        else
                        {
                            if (m_filter.billColor == "0")  // 需要显示蓝字单据
                            {
                                if (record.isRedBill == 0)
                                {
                                    isDisplayRecord = true;
                                }
                            }
                            else if (m_filter.billColor == "1")  // 需要显示红字单据
                            {
                                if (record.isRedBill == 1)
                                {
                                    isDisplayRecord = true;
                                }
                            }
                            else                                // 需要显示全部颜色单据
                            {
                                isDisplayRecord = true;
                            }
                        }
                    }

                    if (isDisplayRecord)
                    {
                        ArrayList temp = new ArrayList();

                        temp.Add(record.pkey);
                        temp.Add("");
                        temp.Add(record.tradingDate);
                        temp.Add(record.billNumber);
                        temp.Add(record.sumValue);
                        temp.Add(record.sumMoney);
                        temp.Add(record.materielOutStaffName);
                        temp.Add(record.makeOrderStaffName);
                        temp.Add(record.orderrReviewName);
                        temp.Add(record.reviewDate);

                        sortedDictionaryList.Add(index, temp);
                    }
                }

                m_dateGridViewExtend.initDataGridViewData(sortedDictionaryList, 3);
            }
        }

        private void billDetail_Click(object sender, EventArgs e)
        {
            checkAccountBillDetaile();
        }

        private void export_Click(object sender, EventArgs e)
        {
            // 此处需要添加导出DataGridViewer数据到Excel的功能
            if (m_dataGridRecordCount > 0)
            {
                this.saveFileDialog1.Filter = "Excel 2007格式 (*.xlsx)|*.xlsx|Excel 2003格式 (*.xls)|*.xls";
                this.saveFileDialog1.RestoreDirectory = true;

                if (saveFileDialog1.ShowDialog() == DialogResult.OK)
                {
                    m_dateGridViewExtend.dataGridViewExportToExecl(saveFileDialog1.FileName);
                }
            }
            else
            {
                MessageBoxExtend.messageWarning("数据为空，无数据可导出!");
            }
        }

        private void print_Click(object sender, EventArgs e)
        {
            m_dateGridViewExtend.printDataGridView();
        }

        private void close_Click(object sender, EventArgs e)
        {
            this.Close();
        }

        private void dataGridViewBilConfigList_Click(object sender, EventArgs e)
        {
            try
            {
                if (m_dataGridRecordCount > 0)
                {
                    // 当单击某个单元格时，自动选择整行
                    for (int i = 0; i < this.dataGridViewList.RowCount; i++)
                    {
                        for (int j = 0; j < dataGridViewList.ColumnCount; j++)
                        {
                            if (dataGridViewList.Rows[i].Cells[j].Selected)
                            {
                                dataGridViewList.Rows[i].Selected = true;
                                m_billNumber = dataGridViewList.Rows[i].Cells[3].Value.ToString();
                                return;
                            }
                        }
                    }
                }
            }
            catch (Exception)
            {
 
            }
        }

        private void dataGridViewMaterielList_DoubleClick(object sender, EventArgs e)
        {
            try
            {
                if (m_dataGridRecordCount > 0)
                {
                    // 当单击某个单元格时，自动选择整行
                    for (int i = 0; i < this.dataGridViewList.RowCount; i++)
                    {
                        for (int j = 0; j < dataGridViewList.ColumnCount; j++)
                        {
                            if (dataGridViewList.Rows[i].Cells[j].Selected)
                            {
                                dataGridViewList.Rows[i].Selected = true;
                                m_billNumber = dataGridViewList.Rows[i].Cells[3].Value.ToString();
                                checkAccountBillDetaile();
                                return;
                            }
                        }
                    }
                }
            }
            catch (Exception)
            {

            }
        }

        private void checkAccountBillDetaile()
        {
            if (m_isSelectOrderNumber)
            {
                this.Close();
                return;
            }
            // checkAccountBillDetaile函数需要完成弹出一个新的窗口，用来显示单据编号关联的具体单据

            if (m_billNumber.Length > 0)
            {
                if (m_orderType == OrderType.SaleOrder || m_orderType == OrderType.SaleOrderExcute)
                {
                    FormSaleOrder fpo = new FormSaleOrder(m_billNumber);
                    fpo.ShowDialog();
                    updateDataGridView();
                }
                else if (m_orderType == OrderType.SaleOut || m_orderType == OrderType.SaleOutOrderExcute)
                {
                    FormSaleOutOrder fpo = new FormSaleOutOrder(m_billNumber);
                    fpo.ShowDialog();
                    updateDataGridView();
                }
                else if (m_orderType == OrderType.SaleInvoice)
                {
                    //销售发票序时薄
                }
                else if (m_orderType == OrderType.SaleQuotation)
                {
                    FormSaleQuotationOrder fsqo = new FormSaleQuotationOrder(m_billNumber);
                    fsqo.ShowDialog();
                    updateDataGridView();
                }
                else if (m_orderType == OrderType.StorageMaterielOut)
                {
                    FormMaterielOutOrder fmoo = new FormMaterielOutOrder(m_billNumber);
                    fmoo.ShowDialog();
                    updateDataGridView();
                }
                else if (m_orderType == OrderType.StorageOutCheck)
                {
                    FormMaterielOutEarningsOrder fmoo = new FormMaterielOutEarningsOrder(m_billNumber);
                    fmoo.ShowDialog();
                    updateDataGridView();
                }
                else if (m_orderType == OrderType.StorageOutOther)
                {
                    FormMaterielOutOtherOrder fmoo = new FormMaterielOutOtherOrder(m_billNumber);
                    fmoo.ShowDialog();
                    updateDataGridView();
                }
                else
                {
                    MessageBoxExtend.messageWarning("暂时不支持的序时薄类型");
                }
            }
        }

        public string getSelectOrderNumber()
        {
            return m_billNumber;
        }

        private string getWindowText(OrderType orderType)
        {
            string winText = "";

            if (m_orderType == OrderType.SaleOrder)
            {
                winText = "销售订单序时薄";
            }
            else if (m_orderType == OrderType.SaleOut)
            {
                winText = "销售出库单序时薄";
            }
            else if (m_orderType == OrderType.SaleInvoice)
            {
                winText = "销售发票序时薄";
            }
            else if (m_orderType == OrderType.SaleOrderExcute)
            {
                winText = "销售订单执行情况";
            }
            else if (m_orderType == OrderType.SaleOutOrderExcute)
            {
                winText = "销售出库收款情况";
            }
            else if (m_orderType == OrderType.SaleQuotation)
            {
                winText = "销售报价单序时薄";
            }
            else if (m_orderType == OrderType.StorageMaterielOut)
            {
                winText = "生产领料单序时薄";
            }
            else if (m_orderType == OrderType.StorageOutCheck)
            {
                winText = "盘亏毁损单序时薄";
            }
            else if (m_orderType == OrderType.StorageOutOther)
            {
                winText = "其他出库单序时薄";
            }
            
            return winText;
        }

        public void setDataFilter(FormStorageSequenceFilterValue filter)
        {
            m_filter = filter;
        }
        #region Panle控件鼠标滑过事件
        private void billDetail_MouseEnter(object sender, EventArgs e)
        {
            this.billDetail.CheckState = CheckState.Checked;
        }

        private void billDetail_MouseLeave(object sender, EventArgs e)
        {
            this.billDetail.CheckState = CheckState.Unchecked;
        }

        private void panelExport_MouseEnter(object sender, EventArgs e)
        {
            this.export.CheckState = CheckState.Checked;
        }

        private void panelExport_MouseLeave(object sender, EventArgs e)
        {
            this.export.CheckState = CheckState.Unchecked;
        }

        private void panelPrintDisplay_MouseEnter(object sender, EventArgs e)
        {
            this.printDisplay.CheckState = CheckState.Checked;
        }

        private void panelPrintDisplay_MouseLeave(object sender, EventArgs e)
        {
            this.printDisplay.CheckState = CheckState.Unchecked;
        }

        private void panelPrint_MouseEnter(object sender, EventArgs e)
        {
            this.print.CheckState = CheckState.Checked;
        }

        private void panelPrint_MouseLeave(object sender, EventArgs e)
        {
            this.print.CheckState = CheckState.Unchecked;
        }

        private void panelImageExit_MouseEnter(object sender, EventArgs e)
        {
            this.close.CheckState = CheckState.Checked;
        }

        private void panelImageExit_MouseLeave(object sender, EventArgs e)
        {
            this.close.CheckState = CheckState.Unchecked;
        }

        #endregion
    }
}