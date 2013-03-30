/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package tinycontrolclient;

/**
 *
 * @author guilherme
 */
public class HistoryEntry {

    private int seq;
    private int prev;
    private int next;
    private int tBefore;
    private int tAfter;

    public HistoryEntry(int seq, int prev, int next, int tBefore, int tAfter) {
        this.seq = seq;
        this.prev = prev;
        this.next = next;
        this.tBefore = tBefore;
        this.tAfter = tAfter;
    }

    public int getSeq() {
        return seq;
    }

    public int getNext() {
        return next;
    }

    public int getPrev() {
        return prev;
    }

    public int gettAfter() {
        return tAfter;
    }

    public int gettBefore() {
        return tBefore;
    }
}
