%Used for plotting signal from HDF5 files from Multichannel Datamanager
%Logan Whitehouse
%lswhiteh@iupui.edu

tmp = matlab.desktop.editor.getActive;
cd(fileparts(tmp.Filename));

%Make sure McsMATLAB Data Tools is installed in MATLAB
%Can be installed from Matlab from App Manager
files = dir('*.h5');

for file = files'
    
    data = McsHDF5.McsData(file.name);
    disp(file.name);
    channelNum = input('Enter channel wanted please: ');
    beginTime = input('Enter beginning time please: ');
    endTime = input('Enter end time please: ');
   
    data.Recording{1}.AnalogStream{1}.Info.Unit{1};
    cfg = [];
    
    %Can put different channels if want to have multiple
    %Just change it to multiple inputs, acts as a range
    cfg.channel = [channelNum channelNum];
    cfg.window = [beginTime endTime];
    partialData = data.Recording{1}.AnalogStream{1}.readPartialChannelData(cfg);
    plot(partialData,[]);
    
    
end