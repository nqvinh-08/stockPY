//tim kiem
const formSearch =document.querySelector("#form-search");

if(formSearch){

    formSearch.addEventListener("submit",(e) =>{ 

        e.preventDefault(); //ngan chan su kien submit mac dinh

        const fromDate = document.getElementById("fromDate").value;
        const toDate = document.getElementById("toDate").value;

        let url = new URL(window.location.href);

        // set fromDate
        if (fromDate) {
            url.searchParams.set("fromDate", fromDate);
        } else {
            url.searchParams.delete("fromDate");
        }
        // set toDate
        if (toDate) {
            url.searchParams.set("toDate", toDate);
        } else {
            url.searchParams.delete("toDate");
        }

        window.location.href = url.href;
    })
}