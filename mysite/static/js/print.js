function winPrint(){
/*	bdhtml = window.document.body.innerHTML;
	startStr = "<!--startprint-->";
	endStr = "<!--endprint-->";
	prnhtml = bdhtml.substr(bdhtml.indexOf(startStr) + 17);
	prnhtml = prnhtml.substring(0,prnhtml.indexOf(endStr));
	window.document.body.innerHTML = prnhtml;*/
	window.print();
	window.document.body.innerHTML = bdhtml;
}
function winJsPrint(){
	$("#jsPrint").jqprint();
}
function doPrint() {
        bdhtml=window.document.body.innerHTML;
        sprnstr="<!--startprint-->";
        prnstr="<!--endprint-->";
        prnhtml=bdhtml.substr(bdhtml.indexOf(sprnstr)+17);
        prnhtml=prnhtml.substring(0,prnhtml.indexOf(eprnstr));
        window.document.body.innerHTML=prnhtml;
        window.print();
    }
function printdiv(printpage) {
    var headhtml = "<html><head><title></title></head><body>";
    var foothtml = "</body>";
    // 获取div中的html内容
    var newhtml = document.all.item(printpage).innerHTML;
    // 获取div中的html内容，jquery写法如下
    // var newhtml= $("#" + printpage).html();

    // 获取原来的窗口界面body的html内容，并保存起来
    var oldhtml = document.body.innerHTML;

    // 给窗口界面重新赋值，赋自己拼接起来的html内容
    document.body.innerHTML = headhtml + newhtml + foothtml;
    // 调用window.print方法打印新窗口
    window.print();

    // 将原来窗口body的html值回填展示
    document.body.innerHTML = oldhtml;
    return false;
}