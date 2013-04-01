/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package tinycontrolclient;

import java.util.ArrayList;
/**
 *
 * @author guilherme
 */
public class History {

    private int currentSeq;
    private int currentTimeStamp;
    private int prevRtt;
    private int recCount;
    private ArrayList<HistoryEntry> entries;
    private ArrayList<Integer> intervals;

    public History() {
        entries = new ArrayList();
        intervals = new ArrayList();
    }
    
    public int getCurrentSeq() {
        return currentSeq;
    }

    public void setCurrentSeq(int currentSeq) {
        this.currentSeq = currentSeq;
    }

    public int getCurrentTimeStamp() {
        return currentTimeStamp;
    }

    public void setCurrentTimeStamp(int currentTimeStamp) {
        this.currentTimeStamp = currentTimeStamp;
    }

    public void addEntry(int seq, int prev, int next, int tBefore, int tAfter) {
        entries.add(new HistoryEntry(seq, prev, next, tBefore, tAfter));
    }
    
    public void removeEntry(int seq) {
        for(int i=0; i<entries.size(); i++) {
            if(entries.get(i).getSeq() == seq) {
                entries.remove(i);
                break;
            }
        }
    }
    
    public void addInterval(int seq) {
        intervals.add(seq);
    }

    public HistoryEntry getLastEntry() {
        return entries.get(entries.size()-1);
    }
    
    public HistoryEntry getLossStarterEntry() {
        return entries.get(intervals.get(intervals.size()-1));
    }

    public ArrayList<Integer> getIntervals() {
        return intervals;
    }

    public int getPrevRtt() {
        return prevRtt;
    }

    public void setPrevRtt(int prevRtt) {
        this.prevRtt = prevRtt;
    }

    public int getRecCount() {
        return recCount;
    }

    public void setRecCount(int recCount) {
        this.recCount = recCount;
    }
}
