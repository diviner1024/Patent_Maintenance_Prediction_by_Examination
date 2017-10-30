clear
clear matrix
set matsize 400
cd "C:\Users\Wenhua Wang\Google Drive\Research\Data_Incubator_chanllenge"
use patent_cost.dta
gen app_date_d = date(app_date, "YMD")
gen iss_date_d = date(iss_date, "YMD")
gen wait_time = (iss_date_d-app_date_d)/365
gen fast_exam = wait_time<1
gen esti_cost = ((rce*1200+max(0,rce-1)*500+800*appeal+500*ret+provison*260+max(pat_indep_clm-3,0)*420+max(pat_indep_clm+pg_dep_clm-20,0)*80+4000*fast_exam)/small_entity)^(1/3)
gen has_pct = pct>=1
gen has_provision = provison>=1
/*keep if pg_indep_clm>0*/
local x rce i.has_provision i.small_entity esti_cost
local y i.has_pct con_parent  appeal ret  pat_indep_clm pat_dep_clm
logistic renew_4  `x' `y'
logistic renew_8  `x' `y'
logistic renew_12  `x'  `y'
