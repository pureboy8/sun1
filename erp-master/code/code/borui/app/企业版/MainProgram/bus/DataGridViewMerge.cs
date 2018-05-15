/// ��DataGridView���кϲ���������
using System;
using System.Collections.Generic;
using System.Text;
using System.Windows.Forms;
using System.Collections;
using System.Drawing;

namespace MainProgram.bus
{
    public class DataGridViewCellMerge
    {
        private static SortedList rowSpan = new SortedList();//ȡ����Ҫ���»��Ƶĵ�Ԫ��
        private static string rowValue = "";//���»��Ƶ��ı�������

        /// <summary>
        /// 
        /// DataGridView�ϲ���Ԫ��(����)
        /// </summary>
        /// <param name="dgv">���Ƶ�DataGridview </param>
        /// <param name="cellArgs">���Ƶ�Ԫ��Ĳ�����DataGridview��CellPainting�¼��в�����</param>
        /// <param name="minColIndex">��ʼ��Ԫ����DataGridView�е�������</param>
        /// <param name="maxColIndex">������Ԫ����DataGridView�е�������</param>
        public static void MerageRowSpan(DataGridView dgv, DataGridViewCellPaintingEventArgs cellArgs, int minColIndex, int maxColIndex)
        {
            if (cellArgs.ColumnIndex < minColIndex || cellArgs.ColumnIndex > maxColIndex) return;

            Rectangle rect=new Rectangle();
            using (Brush gridBrush = new SolidBrush(dgv.GridColor),
                backColorBrush = new SolidBrush(cellArgs.CellStyle.BackColor))
            {
                //Ĩȥԭ����cell����
                cellArgs.Graphics.FillRectangle(backColorBrush, cellArgs.CellBounds);
            }
            cellArgs.Handled = true;

            if (rowSpan[cellArgs.ColumnIndex] == null)
            {
                //�����жϵ�ǰ��Ԫ���ǲ�����Ҫ�ػ�ĵ�Ԫ��
                //�����˵�Ԫ�����Ϣ����Ĩȥ�˵�Ԫ��ı���
                rect.X = cellArgs.CellBounds.X;
                rect.Y = cellArgs.CellBounds.Y;
                rect.Width = cellArgs.CellBounds.Width;
                rect.Height = cellArgs.CellBounds.Height;
                
                rowValue += cellArgs.Value.ToString();
                rowSpan.Add(cellArgs.ColumnIndex, rect);
                if (cellArgs.ColumnIndex != maxColIndex)
                    return;
                MeragePrint(dgv, cellArgs, minColIndex, maxColIndex); 
            }
            else
            {
                IsPostMerage(dgv, cellArgs, minColIndex, maxColIndex);
            }
        }

        public static void IsPostMerage(DataGridView dgv, DataGridViewCellPaintingEventArgs cellArgs, int minColIndex, int maxColIndex)
        {
            //�Ƚϵ�Ԫ�Ƿ��б仯
            Rectangle rectArgs = (Rectangle)rowSpan[cellArgs.ColumnIndex];
            if (rectArgs.X != cellArgs.CellBounds.X || rectArgs.Y != cellArgs.CellBounds.Y
                || rectArgs.Width != cellArgs.CellBounds.Width || rectArgs.Height != cellArgs.CellBounds.Height)
            {
                rectArgs.X = cellArgs.CellBounds.X;
                rectArgs.Y = cellArgs.CellBounds.Y;
                rectArgs.Width = cellArgs.CellBounds.Width;
                rectArgs.Height = cellArgs.CellBounds.Height;
                rowSpan[cellArgs.ColumnIndex] = rectArgs;
            }

            MeragePrint(dgv,cellArgs,minColIndex,maxColIndex);
        }

        //���Ƶ�Ԫ��
        private static void MeragePrint(DataGridView dgv, DataGridViewCellPaintingEventArgs cellArgs, int minColIndex, int maxColIndex)
        {
            int width = 0;//�ϲ���Ԫ���ܿ��
            int height = cellArgs.CellBounds.Height;//�ϲ���Ԫ���ܸ߶�
                
            for (int i = minColIndex; i <= maxColIndex;i++ )
            {
                width += ((Rectangle)rowSpan[i]).Width;
            }

            Rectangle rectBegin = (Rectangle)rowSpan[minColIndex];//�ϲ���һ����Ԫ���λ����Ϣ
            Rectangle rectEnd = (Rectangle)rowSpan[maxColIndex];//�ϲ����һ����Ԫ���λ����Ϣ
                
            //�ϲ���Ԫ���λ����Ϣ
            Rectangle reBounds = new Rectangle();
            reBounds.X = rectBegin.X;
            reBounds.Y = rectBegin.Y;
            reBounds.Width = width - 1;
            reBounds.Height = height - 1;

            using (Brush gridBrush = new SolidBrush(dgv.GridColor), backColorBrush = new SolidBrush(cellArgs.CellStyle.BackColor))
            {
                using (Pen gridLinePen = new Pen(gridBrush))
                {
                    // ���������������ߣ����ұ�����
                    Point blPoint = new Point(rectBegin.Left, rectBegin.Bottom - 1);//�������λ��
                    Point brPoint = new Point(rectEnd.Right - 1, rectEnd.Bottom - 1);//�����ұ�λ��
                    cellArgs.Graphics.DrawLine(gridLinePen, blPoint, brPoint);//�±��� 

                    Point tlPoint = new Point(rectBegin.Left, rectBegin.Top);//�ϱ������λ��
                    Point trPoint = new Point(rectEnd.Right - 1, rectEnd.Top);//�ϱ����ұ�λ��
                    cellArgs.Graphics.DrawLine(gridLinePen, tlPoint, trPoint); //�ϱ���

                    Point ltPoint = new Point(rectBegin.Left, rectBegin.Top);//����߶���λ��
                    Point lbPoint = new Point(rectBegin.Left, rectBegin.Bottom - 1);//����ߵײ�λ��
                    cellArgs.Graphics.DrawLine(gridLinePen, ltPoint, lbPoint); //�����

                    Point rtPoint = new Point(rectEnd.Right - 1, rectEnd.Top);//�ұ��߶���λ��
                    Point rbPoint = new Point(rectEnd.Right - 1, rectEnd.Bottom - 1);//�ұ��ߵײ�λ��
                    cellArgs.Graphics.DrawLine(gridLinePen, rtPoint, rbPoint); //�ұ���

                    //��������ַ�����λ��
                    SizeF sf = cellArgs.Graphics.MeasureString(rowValue, cellArgs.CellStyle.Font);
                    float lstr = (width - sf.Width) / 2;
                    float rstr = (height - sf.Height) / 2;

                    //�����ı���
                    if (rowValue != "")
                    {
                        cellArgs.Graphics.DrawString(rowValue, cellArgs.CellStyle.Font,
                                                    new SolidBrush(cellArgs.CellStyle.ForeColor),
                                                        rectBegin.Left + lstr,
                                                        rectBegin.Top + rstr,
                                                        StringFormat.GenericDefault);
                    }
                }
                cellArgs.Handled = true;
            }
        }
    }
}