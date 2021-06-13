function getEmodel(species)
currentpath = pwd;
cd ../../Results/
for i = 1:length(species)
    display([num2str(i) '/' num2str(length(species))]);
    cd('model_auto')
    z = load([species{i},'_auto.mat']);
    model_auto = z.model;
    enzymedata_auto = z.enzymedata; 

    
    cd('../model_dl')
    z = load([species{i},'_dl.mat']);
    model_DL = z.model;
    enzymedata_DL = z.enzymedata;

    
    cd ../model_bayesian/
    cd(species{i})
    nfound = length(dir('kcat_genra*.txt'));
    if nfound > 0
        tmp = readmatrix(['kcat_genra',num2str(nfound),'.txt'],'FileType','text','Delimiter',',');
        kcat_posterior = tmp(1:end-2,:);
        tot_prot_weight = tmp(end-1,1);
    else
        kcat_posterior = repmat(enzymedata_DL.kcat,1,100);
        [~,tot_prot_weight,~,~,~,~,~,~] = sumBioMass(model_DL);
        tot_prot_weight = tot_prot_weight*0.5;
    end
    
    emodel = convertToGeckoModel(model_auto,enzymedata_auto,tot_prot_weight);
    save([emodel.id,'_auto.mat'],'emodel');
    
    emodel = convertToGeckoModel(model_DL,enzymedata_DL,tot_prot_weight);
    save([emodel.id,'_DL.mat'],'emodel');
    
    ss = num2cell(kcat_posterior',1);
    [a,b] = arrayfun(@updateprior,ss);
    enzymedata_DL.kcat = a';
    emodel = convertToGeckoModel(model_DL,enzymedata_DL,tot_prot_weight);
    save([emodel.id,'_Bayesian_DL_mean.mat'],'emodel');
    
    %for m = 1:length(kcat_posterior(1,:))
    for m = 1:1
        enzymedata_DL.kcat = kcat_posterior(:,m);
        emodel = convertToGeckoModel(model_DL,enzymedata_DL,tot_prot_weight);
        save([emodel.id,num2str(m),'.mat'],'emodel');
    end
    cd ../../
end
cd(currentpath)
end