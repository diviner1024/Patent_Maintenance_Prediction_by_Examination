clear;
load('patent_cost_preliminary.mat')
App_date_num = zeros(length(App_date),1);
Iss_date_num = zeros(length(Iss_date),1);
for i = 1:length(App_date)
    App_date_num(i) = date2num(App_date{i});
    Iss_date_num(i) = date2num(Iss_date{i});
end

pct_mean = zeros(3,5);
k=1;
for i = unique(PCT)'
    pct_mean(1,k) = mean(renew_4(PCT==i))/mean(renew_4);
    pct_mean(2,k) = mean(renew_8(PCT==i))/mean(renew_8);
    pct_mean(3,k) = mean(renew_12(PCT==i))/mean(renew_12);
    k=k+1;
end

con_parent_mean = zeros(3,4);
con_p_bin = [0 1 6 11 inf];
for i = 1:4
    con_index = Con_Parent>=con_p_bin(i)&Con_Parent<con_p_bin(i+1);
    con_parent_mean(1,i) = mean(renew_4(con_index))/mean(renew_4);
    con_parent_mean(2,i) = mean(renew_8(con_index))/mean(renew_8);
    con_parent_mean(3,i) = mean(renew_12(con_index))/mean(renew_12);
end

con_child_mean = zeros(3,3);
con_p_bin = [0 1 2 inf];
for i = 1:3
    con_index = Con_child>=con_p_bin(i)&Con_child<con_p_bin(i+1);
    con_child_mean(1,i) = mean(renew_4(con_index))/mean(renew_4);
    con_child_mean(2,i) = mean(renew_8(con_index))/mean(renew_8);
    con_child_mean(3,i) = mean(renew_12(con_index))/mean(renew_12);
end

wait_time = Iss_date_num-App_date_num;
wait_bin = [(0:5)*365 inf];
wait_mean = zeros(3,6);
for i = 1:6
    wait_index = wait_time>=wait_bin(i)&wait_time<wait_bin(i+1);
    wait_mean(1,i) = mean(renew_4(wait_index))/mean(renew_4);
    wait_mean(2,i) = mean(renew_8(wait_index))/mean(renew_8);
    wait_mean(3,i) = mean(renew_12(wait_index))/mean(renew_12);
end

appeal_bin = [0 1 inf];
appeal_mean = zeros(3,2);
for i = 1:2
    appeal_index = Appeal>=appeal_bin(i)&Appeal<appeal_bin(i+1);
    appeal_mean(1,i) = mean(renew_4(appeal_index))/mean(renew_4);
    appeal_mean(2,i) = mean(renew_8(appeal_index))/mean(renew_8);
    appeal_mean(3,i) = mean(renew_12(appeal_index))/mean(renew_12);
end

rce_bin = [0 1 2 inf];
rce_mean = zeros(3,3);
for i = 1:3
    rce_index = RCE>=rce_bin(i)&RCE<=rce_bin(i+1);
    rce_mean(1,i) = mean(renew_4(rce_index))/mean(renew_4);
    rce_mean(2,i) = mean(renew_8(rce_index))/mean(renew_8);
    rce_mean(3,i) = mean(renew_12(rce_index))/mean(renew_12);
end

pro_bin = [0 1 2 inf];
pro_mean = zeros(3,3);
for i = 1:3
    rce_index = Provision>=pro_bin(i)&Provision<=pro_bin(i+1);
    pro_mean(1,i) = mean(renew_4(rce_index))/mean(renew_4);
    pro_mean(2,i) = mean(renew_8(rce_index))/mean(renew_8);
    pro_mean(3,i) = mean(renew_12(rce_index))/mean(renew_12);
end


small_mean = zeros(3,3);
for i = 1:3
    small_mean(1,i) = mean(renew_4(small_entity==(2^(i-1))))/mean(renew_4);
    small_mean(2,i) = mean(renew_8(small_entity==(2^(i-1))))/mean(renew_8);
    small_mean(3,i) = mean(renew_12(small_entity==(2^(i-1))))/mean(renew_12);
end

figure(1)
colormap autumn
subplot(1,3,1)
bar(rce_mean)
ylabel('Renewal odds vs. baseline','fontsize',12)
ylim([0.9 1.15])
legend('No RCE','One RCE','Two or more','location','northwest')
title('Request for Continued Examination')
set(gca,'XTickLabel',{'Year 4','Year 8','Year 12'})
set(gca,'fontsize',11)
subplot(1,3,2)
bar(pro_mean)
ylabel('Renewal odds vs. baseline','fontsize',12)
ylim([0.9 1.2])
legend('No Pro','One Pro','Two or more','location','northwest')
title('Provisional Application')
set(gca,'XTickLabel',{'Year 4','Year 8','Year 12'})
set(gca,'fontsize',11)
subplot(1,3,3)
bar(small_mean)
ylabel('Renewal odds vs. baseline','fontsize',12)
ylim([0.5 1.5])
legend('Large','Small','Micro','location','northwest')
title('Application Entity')
set(gca,'XTickLabel',{'Year 4','Year 8','Year 12'})
set(gca,'fontsize',11)
set(gcf,'PaperUnits','inches','PaperPosition',[0.1 0.1 12 6],'PaperSize',[12.1 6.1]);
print('renewal_odds_vs_conditions.png','-dpng')