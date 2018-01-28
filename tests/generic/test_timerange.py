import pytest

from datetime import datetime, time

from firewall_translator.generic import TimeRange, AbsoluteTimeRange, PeriodicTimeRange


def test_time_range_not_implemented():
    with pytest.raises(NotImplementedError):
        t = TimeRange()


@pytest.mark.parametrize('t_start, t_stop, t_repr, t_str',
                         [
                             (datetime(2018, 1, 2), datetime(2018, 1, 1), 'RuntimeError', 'RuntimeError'),
                             (datetime(2017, 12, 25), datetime(2018, 1, 1, 23, 59, 59, 999999), '<AbsoluteTimeRange 2017-12-25T00:00 2018-01-01T23:59>', 'from 2017-12-25 00:00 to 2018-01-01 23:59'),
                         ])
def test_absolute_time_range(t_start, t_stop, t_repr, t_str):
    if t_start > t_stop:
        with pytest.raises(RuntimeError):
            t = AbsoluteTimeRange(t_start, t_stop)

    else:
        t = AbsoluteTimeRange(t_start, t_stop)
        assert t.start == t_start
        assert t.stop == t_stop
        assert repr(t) == t_repr
        assert str(t) == t_str


@pytest.mark.parametrize('t_start, t_stop, t_weekdays, t_repr, t_str',
                         [
                             (time(1), time(0), [False, False, False, False, False, False, False], 'RuntimeError', 'RuntimeError'),
                             (time(0), time(23, 59, 59, 999999), [False, False, False, False, False, False, False], 'RuntimeError', 'RuntimeError'),
                             (time(0), time(23, 59, 59, 999999), [False, False, False, False, False, False, True], '<PeriodicTimeRange 00:00 23:59 [False, False, False, False, False, False, True]>', 'from 00:00 to 23:59 on sat'),
                             (time(0), time(23, 59, 59, 999999), [False, False, False, False, False, True, False], '<PeriodicTimeRange 00:00 23:59 [False, False, False, False, False, True, False]>', 'from 00:00 to 23:59 on fri'),
                             (time(0), time(23, 59, 59, 999999), [False, False, False, False, False, True, True], '<PeriodicTimeRange 00:00 23:59 [False, False, False, False, False, True, True]>', 'from 00:00 to 23:59 on fri, sat'),
                             (time(0), time(23, 59, 59, 999999), [False, False, False, False, True, False, False], '<PeriodicTimeRange 00:00 23:59 [False, False, False, False, True, False, False]>', 'from 00:00 to 23:59 on thu'),
                             (time(0), time(23, 59, 59, 999999), [False, False, False, False, True, False, True], '<PeriodicTimeRange 00:00 23:59 [False, False, False, False, True, False, True]>', 'from 00:00 to 23:59 on thu, sat'),
                             (time(0), time(23, 59, 59, 999999), [False, False, False, False, True, True, False], '<PeriodicTimeRange 00:00 23:59 [False, False, False, False, True, True, False]>', 'from 00:00 to 23:59 on thu, fri'),
                             (time(0), time(23, 59, 59, 999999), [False, False, False, False, True, True, True], '<PeriodicTimeRange 00:00 23:59 [False, False, False, False, True, True, True]>', 'from 00:00 to 23:59 on thu, fri, sat'),
                             (time(0), time(23, 59, 59, 999999), [False, False, False, True, False, False, False], '<PeriodicTimeRange 00:00 23:59 [False, False, False, True, False, False, False]>', 'from 00:00 to 23:59 on wed'),
                             (time(0), time(23, 59, 59, 999999), [False, False, False, True, False, False, True], '<PeriodicTimeRange 00:00 23:59 [False, False, False, True, False, False, True]>', 'from 00:00 to 23:59 on wed, sat'),
                             (time(0), time(23, 59, 59, 999999), [False, False, False, True, False, True, False], '<PeriodicTimeRange 00:00 23:59 [False, False, False, True, False, True, False]>', 'from 00:00 to 23:59 on wed, fri'),
                             (time(0), time(23, 59, 59, 999999), [False, False, False, True, False, True, True], '<PeriodicTimeRange 00:00 23:59 [False, False, False, True, False, True, True]>', 'from 00:00 to 23:59 on wed, fri, sat'),
                             (time(0), time(23, 59, 59, 999999), [False, False, False, True, True, False, False], '<PeriodicTimeRange 00:00 23:59 [False, False, False, True, True, False, False]>', 'from 00:00 to 23:59 on wed, thu'),
                             (time(0), time(23, 59, 59, 999999), [False, False, False, True, True, False, True], '<PeriodicTimeRange 00:00 23:59 [False, False, False, True, True, False, True]>', 'from 00:00 to 23:59 on wed, thu, sat'),
                             (time(0), time(23, 59, 59, 999999), [False, False, False, True, True, True, False], '<PeriodicTimeRange 00:00 23:59 [False, False, False, True, True, True, False]>', 'from 00:00 to 23:59 on wed, thu, fri'),
                             (time(0), time(23, 59, 59, 999999), [False, False, False, True, True, True, True], '<PeriodicTimeRange 00:00 23:59 [False, False, False, True, True, True, True]>', 'from 00:00 to 23:59 on wed, thu, fri, sat'),
                             (time(0), time(23, 59, 59, 999999), [False, False, True, False, False, False, False], '<PeriodicTimeRange 00:00 23:59 [False, False, True, False, False, False, False]>', 'from 00:00 to 23:59 on tue'),
                             (time(0), time(23, 59, 59, 999999), [False, False, True, False, False, False, True], '<PeriodicTimeRange 00:00 23:59 [False, False, True, False, False, False, True]>', 'from 00:00 to 23:59 on tue, sat'),
                             (time(0), time(23, 59, 59, 999999), [False, False, True, False, False, True, False], '<PeriodicTimeRange 00:00 23:59 [False, False, True, False, False, True, False]>', 'from 00:00 to 23:59 on tue, fri'),
                             (time(0), time(23, 59, 59, 999999), [False, False, True, False, False, True, True], '<PeriodicTimeRange 00:00 23:59 [False, False, True, False, False, True, True]>', 'from 00:00 to 23:59 on tue, fri, sat'),
                             (time(0), time(23, 59, 59, 999999), [False, False, True, False, True, False, False], '<PeriodicTimeRange 00:00 23:59 [False, False, True, False, True, False, False]>', 'from 00:00 to 23:59 on tue, thu'),
                             (time(0), time(23, 59, 59, 999999), [False, False, True, False, True, False, True], '<PeriodicTimeRange 00:00 23:59 [False, False, True, False, True, False, True]>', 'from 00:00 to 23:59 on tue, thu, sat'),
                             (time(0), time(23, 59, 59, 999999), [False, False, True, False, True, True, False], '<PeriodicTimeRange 00:00 23:59 [False, False, True, False, True, True, False]>', 'from 00:00 to 23:59 on tue, thu, fri'),
                             (time(0), time(23, 59, 59, 999999), [False, False, True, False, True, True, True], '<PeriodicTimeRange 00:00 23:59 [False, False, True, False, True, True, True]>', 'from 00:00 to 23:59 on tue, thu, fri, sat'),
                             (time(0), time(23, 59, 59, 999999), [False, False, True, True, False, False, False], '<PeriodicTimeRange 00:00 23:59 [False, False, True, True, False, False, False]>', 'from 00:00 to 23:59 on tue, wed'),
                             (time(0), time(23, 59, 59, 999999), [False, False, True, True, False, False, True], '<PeriodicTimeRange 00:00 23:59 [False, False, True, True, False, False, True]>', 'from 00:00 to 23:59 on tue, wed, sat'),
                             (time(0), time(23, 59, 59, 999999), [False, False, True, True, False, True, False], '<PeriodicTimeRange 00:00 23:59 [False, False, True, True, False, True, False]>', 'from 00:00 to 23:59 on tue, wed, fri'),
                             (time(0), time(23, 59, 59, 999999), [False, False, True, True, False, True, True], '<PeriodicTimeRange 00:00 23:59 [False, False, True, True, False, True, True]>', 'from 00:00 to 23:59 on tue, wed, fri, sat'),
                             (time(0), time(23, 59, 59, 999999), [False, False, True, True, True, False, False], '<PeriodicTimeRange 00:00 23:59 [False, False, True, True, True, False, False]>', 'from 00:00 to 23:59 on tue, wed, thu'),
                             (time(0), time(23, 59, 59, 999999), [False, False, True, True, True, False, True], '<PeriodicTimeRange 00:00 23:59 [False, False, True, True, True, False, True]>', 'from 00:00 to 23:59 on tue, wed, thu, sat'),
                             (time(0), time(23, 59, 59, 999999), [False, False, True, True, True, True, False], '<PeriodicTimeRange 00:00 23:59 [False, False, True, True, True, True, False]>', 'from 00:00 to 23:59 on tue, wed, thu, fri'),
                             (time(0), time(23, 59, 59, 999999), [False, False, True, True, True, True, True], '<PeriodicTimeRange 00:00 23:59 [False, False, True, True, True, True, True]>', 'from 00:00 to 23:59 on tue, wed, thu, fri, sat'),
                             (time(0), time(23, 59, 59, 999999), [False, True, False, False, False, False, False], '<PeriodicTimeRange 00:00 23:59 [False, True, False, False, False, False, False]>', 'from 00:00 to 23:59 on mon'),
                             (time(0), time(23, 59, 59, 999999), [False, True, False, False, False, False, True], '<PeriodicTimeRange 00:00 23:59 [False, True, False, False, False, False, True]>', 'from 00:00 to 23:59 on mon, sat'),
                             (time(0), time(23, 59, 59, 999999), [False, True, False, False, False, True, False], '<PeriodicTimeRange 00:00 23:59 [False, True, False, False, False, True, False]>', 'from 00:00 to 23:59 on mon, fri'),
                             (time(0), time(23, 59, 59, 999999), [False, True, False, False, False, True, True], '<PeriodicTimeRange 00:00 23:59 [False, True, False, False, False, True, True]>', 'from 00:00 to 23:59 on mon, fri, sat'),
                             (time(0), time(23, 59, 59, 999999), [False, True, False, False, True, False, False], '<PeriodicTimeRange 00:00 23:59 [False, True, False, False, True, False, False]>', 'from 00:00 to 23:59 on mon, thu'),
                             (time(0), time(23, 59, 59, 999999), [False, True, False, False, True, False, True], '<PeriodicTimeRange 00:00 23:59 [False, True, False, False, True, False, True]>', 'from 00:00 to 23:59 on mon, thu, sat'),
                             (time(0), time(23, 59, 59, 999999), [False, True, False, False, True, True, False], '<PeriodicTimeRange 00:00 23:59 [False, True, False, False, True, True, False]>', 'from 00:00 to 23:59 on mon, thu, fri'),
                             (time(0), time(23, 59, 59, 999999), [False, True, False, False, True, True, True], '<PeriodicTimeRange 00:00 23:59 [False, True, False, False, True, True, True]>', 'from 00:00 to 23:59 on mon, thu, fri, sat'),
                             (time(0), time(23, 59, 59, 999999), [False, True, False, True, False, False, False], '<PeriodicTimeRange 00:00 23:59 [False, True, False, True, False, False, False]>', 'from 00:00 to 23:59 on mon, wed'),
                             (time(0), time(23, 59, 59, 999999), [False, True, False, True, False, False, True], '<PeriodicTimeRange 00:00 23:59 [False, True, False, True, False, False, True]>', 'from 00:00 to 23:59 on mon, wed, sat'),
                             (time(0), time(23, 59, 59, 999999), [False, True, False, True, False, True, False], '<PeriodicTimeRange 00:00 23:59 [False, True, False, True, False, True, False]>', 'from 00:00 to 23:59 on mon, wed, fri'),
                             (time(0), time(23, 59, 59, 999999), [False, True, False, True, False, True, True], '<PeriodicTimeRange 00:00 23:59 [False, True, False, True, False, True, True]>', 'from 00:00 to 23:59 on mon, wed, fri, sat'),
                             (time(0), time(23, 59, 59, 999999), [False, True, False, True, True, False, False], '<PeriodicTimeRange 00:00 23:59 [False, True, False, True, True, False, False]>', 'from 00:00 to 23:59 on mon, wed, thu'),
                             (time(0), time(23, 59, 59, 999999), [False, True, False, True, True, False, True], '<PeriodicTimeRange 00:00 23:59 [False, True, False, True, True, False, True]>', 'from 00:00 to 23:59 on mon, wed, thu, sat'),
                             (time(0), time(23, 59, 59, 999999), [False, True, False, True, True, True, False], '<PeriodicTimeRange 00:00 23:59 [False, True, False, True, True, True, False]>', 'from 00:00 to 23:59 on mon, wed, thu, fri'),
                             (time(0), time(23, 59, 59, 999999), [False, True, False, True, True, True, True], '<PeriodicTimeRange 00:00 23:59 [False, True, False, True, True, True, True]>', 'from 00:00 to 23:59 on mon, wed, thu, fri, sat'),
                             (time(0), time(23, 59, 59, 999999), [False, True, True, False, False, False, False], '<PeriodicTimeRange 00:00 23:59 [False, True, True, False, False, False, False]>', 'from 00:00 to 23:59 on mon, tue'),
                             (time(0), time(23, 59, 59, 999999), [False, True, True, False, False, False, True], '<PeriodicTimeRange 00:00 23:59 [False, True, True, False, False, False, True]>', 'from 00:00 to 23:59 on mon, tue, sat'),
                             (time(0), time(23, 59, 59, 999999), [False, True, True, False, False, True, False], '<PeriodicTimeRange 00:00 23:59 [False, True, True, False, False, True, False]>', 'from 00:00 to 23:59 on mon, tue, fri'),
                             (time(0), time(23, 59, 59, 999999), [False, True, True, False, False, True, True], '<PeriodicTimeRange 00:00 23:59 [False, True, True, False, False, True, True]>', 'from 00:00 to 23:59 on mon, tue, fri, sat'),
                             (time(0), time(23, 59, 59, 999999), [False, True, True, False, True, False, False], '<PeriodicTimeRange 00:00 23:59 [False, True, True, False, True, False, False]>', 'from 00:00 to 23:59 on mon, tue, thu'),
                             (time(0), time(23, 59, 59, 999999), [False, True, True, False, True, False, True], '<PeriodicTimeRange 00:00 23:59 [False, True, True, False, True, False, True]>', 'from 00:00 to 23:59 on mon, tue, thu, sat'),
                             (time(0), time(23, 59, 59, 999999), [False, True, True, False, True, True, False], '<PeriodicTimeRange 00:00 23:59 [False, True, True, False, True, True, False]>', 'from 00:00 to 23:59 on mon, tue, thu, fri'),
                             (time(0), time(23, 59, 59, 999999), [False, True, True, False, True, True, True], '<PeriodicTimeRange 00:00 23:59 [False, True, True, False, True, True, True]>', 'from 00:00 to 23:59 on mon, tue, thu, fri, sat'),
                             (time(0), time(23, 59, 59, 999999), [False, True, True, True, False, False, False], '<PeriodicTimeRange 00:00 23:59 [False, True, True, True, False, False, False]>', 'from 00:00 to 23:59 on mon, tue, wed'),
                             (time(0), time(23, 59, 59, 999999), [False, True, True, True, False, False, True], '<PeriodicTimeRange 00:00 23:59 [False, True, True, True, False, False, True]>', 'from 00:00 to 23:59 on mon, tue, wed, sat'),
                             (time(0), time(23, 59, 59, 999999), [False, True, True, True, False, True, False], '<PeriodicTimeRange 00:00 23:59 [False, True, True, True, False, True, False]>', 'from 00:00 to 23:59 on mon, tue, wed, fri'),
                             (time(0), time(23, 59, 59, 999999), [False, True, True, True, False, True, True], '<PeriodicTimeRange 00:00 23:59 [False, True, True, True, False, True, True]>', 'from 00:00 to 23:59 on mon, tue, wed, fri, sat'),
                             (time(0), time(23, 59, 59, 999999), [False, True, True, True, True, False, False], '<PeriodicTimeRange 00:00 23:59 [False, True, True, True, True, False, False]>', 'from 00:00 to 23:59 on mon, tue, wed, thu'),
                             (time(0), time(23, 59, 59, 999999), [False, True, True, True, True, False, True], '<PeriodicTimeRange 00:00 23:59 [False, True, True, True, True, False, True]>', 'from 00:00 to 23:59 on mon, tue, wed, thu, sat'),
                             (time(0), time(23, 59, 59, 999999), [False, True, True, True, True, True, False], '<PeriodicTimeRange 00:00 23:59 [False, True, True, True, True, True, False]>', 'from 00:00 to 23:59 on mon, tue, wed, thu, fri'),
                             (time(0), time(23, 59, 59, 999999), [False, True, True, True, True, True, True], '<PeriodicTimeRange 00:00 23:59 [False, True, True, True, True, True, True]>', 'from 00:00 to 23:59 on mon, tue, wed, thu, fri, sat'),
                             (time(0), time(23, 59, 59, 999999), [True, False, False, False, False, False, False], '<PeriodicTimeRange 00:00 23:59 [True, False, False, False, False, False, False]>', 'from 00:00 to 23:59 on sun'),
                             (time(0), time(23, 59, 59, 999999), [True, False, False, False, False, False, True], '<PeriodicTimeRange 00:00 23:59 [True, False, False, False, False, False, True]>', 'from 00:00 to 23:59 on sun, sat'),
                             (time(0), time(23, 59, 59, 999999), [True, False, False, False, False, True, False], '<PeriodicTimeRange 00:00 23:59 [True, False, False, False, False, True, False]>', 'from 00:00 to 23:59 on sun, fri'),
                             (time(0), time(23, 59, 59, 999999), [True, False, False, False, False, True, True], '<PeriodicTimeRange 00:00 23:59 [True, False, False, False, False, True, True]>', 'from 00:00 to 23:59 on sun, fri, sat'),
                             (time(0), time(23, 59, 59, 999999), [True, False, False, False, True, False, False], '<PeriodicTimeRange 00:00 23:59 [True, False, False, False, True, False, False]>', 'from 00:00 to 23:59 on sun, thu'),
                             (time(0), time(23, 59, 59, 999999), [True, False, False, False, True, False, True], '<PeriodicTimeRange 00:00 23:59 [True, False, False, False, True, False, True]>', 'from 00:00 to 23:59 on sun, thu, sat'),
                             (time(0), time(23, 59, 59, 999999), [True, False, False, False, True, True, False], '<PeriodicTimeRange 00:00 23:59 [True, False, False, False, True, True, False]>', 'from 00:00 to 23:59 on sun, thu, fri'),
                             (time(0), time(23, 59, 59, 999999), [True, False, False, False, True, True, True], '<PeriodicTimeRange 00:00 23:59 [True, False, False, False, True, True, True]>', 'from 00:00 to 23:59 on sun, thu, fri, sat'),
                             (time(0), time(23, 59, 59, 999999), [True, False, False, True, False, False, False], '<PeriodicTimeRange 00:00 23:59 [True, False, False, True, False, False, False]>', 'from 00:00 to 23:59 on sun, wed'),
                             (time(0), time(23, 59, 59, 999999), [True, False, False, True, False, False, True], '<PeriodicTimeRange 00:00 23:59 [True, False, False, True, False, False, True]>', 'from 00:00 to 23:59 on sun, wed, sat'),
                             (time(0), time(23, 59, 59, 999999), [True, False, False, True, False, True, False], '<PeriodicTimeRange 00:00 23:59 [True, False, False, True, False, True, False]>', 'from 00:00 to 23:59 on sun, wed, fri'),
                             (time(0), time(23, 59, 59, 999999), [True, False, False, True, False, True, True], '<PeriodicTimeRange 00:00 23:59 [True, False, False, True, False, True, True]>', 'from 00:00 to 23:59 on sun, wed, fri, sat'),
                             (time(0), time(23, 59, 59, 999999), [True, False, False, True, True, False, False], '<PeriodicTimeRange 00:00 23:59 [True, False, False, True, True, False, False]>', 'from 00:00 to 23:59 on sun, wed, thu'),
                             (time(0), time(23, 59, 59, 999999), [True, False, False, True, True, False, True], '<PeriodicTimeRange 00:00 23:59 [True, False, False, True, True, False, True]>', 'from 00:00 to 23:59 on sun, wed, thu, sat'),
                             (time(0), time(23, 59, 59, 999999), [True, False, False, True, True, True, False], '<PeriodicTimeRange 00:00 23:59 [True, False, False, True, True, True, False]>', 'from 00:00 to 23:59 on sun, wed, thu, fri'),
                             (time(0), time(23, 59, 59, 999999), [True, False, False, True, True, True, True], '<PeriodicTimeRange 00:00 23:59 [True, False, False, True, True, True, True]>', 'from 00:00 to 23:59 on sun, wed, thu, fri, sat'),
                             (time(0), time(23, 59, 59, 999999), [True, False, True, False, False, False, False], '<PeriodicTimeRange 00:00 23:59 [True, False, True, False, False, False, False]>', 'from 00:00 to 23:59 on sun, tue'),
                             (time(0), time(23, 59, 59, 999999), [True, False, True, False, False, False, True], '<PeriodicTimeRange 00:00 23:59 [True, False, True, False, False, False, True]>', 'from 00:00 to 23:59 on sun, tue, sat'),
                             (time(0), time(23, 59, 59, 999999), [True, False, True, False, False, True, False], '<PeriodicTimeRange 00:00 23:59 [True, False, True, False, False, True, False]>', 'from 00:00 to 23:59 on sun, tue, fri'),
                             (time(0), time(23, 59, 59, 999999), [True, False, True, False, False, True, True], '<PeriodicTimeRange 00:00 23:59 [True, False, True, False, False, True, True]>', 'from 00:00 to 23:59 on sun, tue, fri, sat'),
                             (time(0), time(23, 59, 59, 999999), [True, False, True, False, True, False, False], '<PeriodicTimeRange 00:00 23:59 [True, False, True, False, True, False, False]>', 'from 00:00 to 23:59 on sun, tue, thu'),
                             (time(0), time(23, 59, 59, 999999), [True, False, True, False, True, False, True], '<PeriodicTimeRange 00:00 23:59 [True, False, True, False, True, False, True]>', 'from 00:00 to 23:59 on sun, tue, thu, sat'),
                             (time(0), time(23, 59, 59, 999999), [True, False, True, False, True, True, False], '<PeriodicTimeRange 00:00 23:59 [True, False, True, False, True, True, False]>', 'from 00:00 to 23:59 on sun, tue, thu, fri'),
                             (time(0), time(23, 59, 59, 999999), [True, False, True, False, True, True, True], '<PeriodicTimeRange 00:00 23:59 [True, False, True, False, True, True, True]>', 'from 00:00 to 23:59 on sun, tue, thu, fri, sat'),
                             (time(0), time(23, 59, 59, 999999), [True, False, True, True, False, False, False], '<PeriodicTimeRange 00:00 23:59 [True, False, True, True, False, False, False]>', 'from 00:00 to 23:59 on sun, tue, wed'),
                             (time(0), time(23, 59, 59, 999999), [True, False, True, True, False, False, True], '<PeriodicTimeRange 00:00 23:59 [True, False, True, True, False, False, True]>', 'from 00:00 to 23:59 on sun, tue, wed, sat'),
                             (time(0), time(23, 59, 59, 999999), [True, False, True, True, False, True, False], '<PeriodicTimeRange 00:00 23:59 [True, False, True, True, False, True, False]>', 'from 00:00 to 23:59 on sun, tue, wed, fri'),
                             (time(0), time(23, 59, 59, 999999), [True, False, True, True, False, True, True], '<PeriodicTimeRange 00:00 23:59 [True, False, True, True, False, True, True]>', 'from 00:00 to 23:59 on sun, tue, wed, fri, sat'),
                             (time(0), time(23, 59, 59, 999999), [True, False, True, True, True, False, False], '<PeriodicTimeRange 00:00 23:59 [True, False, True, True, True, False, False]>', 'from 00:00 to 23:59 on sun, tue, wed, thu'),
                             (time(0), time(23, 59, 59, 999999), [True, False, True, True, True, False, True], '<PeriodicTimeRange 00:00 23:59 [True, False, True, True, True, False, True]>', 'from 00:00 to 23:59 on sun, tue, wed, thu, sat'),
                             (time(0), time(23, 59, 59, 999999), [True, False, True, True, True, True, False], '<PeriodicTimeRange 00:00 23:59 [True, False, True, True, True, True, False]>', 'from 00:00 to 23:59 on sun, tue, wed, thu, fri'),
                             (time(0), time(23, 59, 59, 999999), [True, False, True, True, True, True, True], '<PeriodicTimeRange 00:00 23:59 [True, False, True, True, True, True, True]>', 'from 00:00 to 23:59 on sun, tue, wed, thu, fri, sat'),
                             (time(0), time(23, 59, 59, 999999), [True, True, False, False, False, False, False], '<PeriodicTimeRange 00:00 23:59 [True, True, False, False, False, False, False]>', 'from 00:00 to 23:59 on sun, mon'),
                             (time(0), time(23, 59, 59, 999999), [True, True, False, False, False, False, True], '<PeriodicTimeRange 00:00 23:59 [True, True, False, False, False, False, True]>', 'from 00:00 to 23:59 on sun, mon, sat'),
                             (time(0), time(23, 59, 59, 999999), [True, True, False, False, False, True, False], '<PeriodicTimeRange 00:00 23:59 [True, True, False, False, False, True, False]>', 'from 00:00 to 23:59 on sun, mon, fri'),
                             (time(0), time(23, 59, 59, 999999), [True, True, False, False, False, True, True], '<PeriodicTimeRange 00:00 23:59 [True, True, False, False, False, True, True]>', 'from 00:00 to 23:59 on sun, mon, fri, sat'),
                             (time(0), time(23, 59, 59, 999999), [True, True, False, False, True, False, False], '<PeriodicTimeRange 00:00 23:59 [True, True, False, False, True, False, False]>', 'from 00:00 to 23:59 on sun, mon, thu'),
                             (time(0), time(23, 59, 59, 999999), [True, True, False, False, True, False, True], '<PeriodicTimeRange 00:00 23:59 [True, True, False, False, True, False, True]>', 'from 00:00 to 23:59 on sun, mon, thu, sat'),
                             (time(0), time(23, 59, 59, 999999), [True, True, False, False, True, True, False], '<PeriodicTimeRange 00:00 23:59 [True, True, False, False, True, True, False]>', 'from 00:00 to 23:59 on sun, mon, thu, fri'),
                             (time(0), time(23, 59, 59, 999999), [True, True, False, False, True, True, True], '<PeriodicTimeRange 00:00 23:59 [True, True, False, False, True, True, True]>', 'from 00:00 to 23:59 on sun, mon, thu, fri, sat'),
                             (time(0), time(23, 59, 59, 999999), [True, True, False, True, False, False, False], '<PeriodicTimeRange 00:00 23:59 [True, True, False, True, False, False, False]>', 'from 00:00 to 23:59 on sun, mon, wed'),
                             (time(0), time(23, 59, 59, 999999), [True, True, False, True, False, False, True], '<PeriodicTimeRange 00:00 23:59 [True, True, False, True, False, False, True]>', 'from 00:00 to 23:59 on sun, mon, wed, sat'),
                             (time(0), time(23, 59, 59, 999999), [True, True, False, True, False, True, False], '<PeriodicTimeRange 00:00 23:59 [True, True, False, True, False, True, False]>', 'from 00:00 to 23:59 on sun, mon, wed, fri'),
                             (time(0), time(23, 59, 59, 999999), [True, True, False, True, False, True, True], '<PeriodicTimeRange 00:00 23:59 [True, True, False, True, False, True, True]>', 'from 00:00 to 23:59 on sun, mon, wed, fri, sat'),
                             (time(0), time(23, 59, 59, 999999), [True, True, False, True, True, False, False], '<PeriodicTimeRange 00:00 23:59 [True, True, False, True, True, False, False]>', 'from 00:00 to 23:59 on sun, mon, wed, thu'),
                             (time(0), time(23, 59, 59, 999999), [True, True, False, True, True, False, True], '<PeriodicTimeRange 00:00 23:59 [True, True, False, True, True, False, True]>', 'from 00:00 to 23:59 on sun, mon, wed, thu, sat'),
                             (time(0), time(23, 59, 59, 999999), [True, True, False, True, True, True, False], '<PeriodicTimeRange 00:00 23:59 [True, True, False, True, True, True, False]>', 'from 00:00 to 23:59 on sun, mon, wed, thu, fri'),
                             (time(0), time(23, 59, 59, 999999), [True, True, False, True, True, True, True], '<PeriodicTimeRange 00:00 23:59 [True, True, False, True, True, True, True]>', 'from 00:00 to 23:59 on sun, mon, wed, thu, fri, sat'),
                             (time(0), time(23, 59, 59, 999999), [True, True, True, False, False, False, False], '<PeriodicTimeRange 00:00 23:59 [True, True, True, False, False, False, False]>', 'from 00:00 to 23:59 on sun, mon, tue'),
                             (time(0), time(23, 59, 59, 999999), [True, True, True, False, False, False, True], '<PeriodicTimeRange 00:00 23:59 [True, True, True, False, False, False, True]>', 'from 00:00 to 23:59 on sun, mon, tue, sat'),
                             (time(0), time(23, 59, 59, 999999), [True, True, True, False, False, True, False], '<PeriodicTimeRange 00:00 23:59 [True, True, True, False, False, True, False]>', 'from 00:00 to 23:59 on sun, mon, tue, fri'),
                             (time(0), time(23, 59, 59, 999999), [True, True, True, False, False, True, True], '<PeriodicTimeRange 00:00 23:59 [True, True, True, False, False, True, True]>', 'from 00:00 to 23:59 on sun, mon, tue, fri, sat'),
                             (time(0), time(23, 59, 59, 999999), [True, True, True, False, True, False, False], '<PeriodicTimeRange 00:00 23:59 [True, True, True, False, True, False, False]>', 'from 00:00 to 23:59 on sun, mon, tue, thu'),
                             (time(0), time(23, 59, 59, 999999), [True, True, True, False, True, False, True], '<PeriodicTimeRange 00:00 23:59 [True, True, True, False, True, False, True]>', 'from 00:00 to 23:59 on sun, mon, tue, thu, sat'),
                             (time(0), time(23, 59, 59, 999999), [True, True, True, False, True, True, False], '<PeriodicTimeRange 00:00 23:59 [True, True, True, False, True, True, False]>', 'from 00:00 to 23:59 on sun, mon, tue, thu, fri'),
                             (time(0), time(23, 59, 59, 999999), [True, True, True, False, True, True, True], '<PeriodicTimeRange 00:00 23:59 [True, True, True, False, True, True, True]>', 'from 00:00 to 23:59 on sun, mon, tue, thu, fri, sat'),
                             (time(0), time(23, 59, 59, 999999), [True, True, True, True, False, False, False], '<PeriodicTimeRange 00:00 23:59 [True, True, True, True, False, False, False]>', 'from 00:00 to 23:59 on sun, mon, tue, wed'),
                             (time(0), time(23, 59, 59, 999999), [True, True, True, True, False, False, True], '<PeriodicTimeRange 00:00 23:59 [True, True, True, True, False, False, True]>', 'from 00:00 to 23:59 on sun, mon, tue, wed, sat'),
                             (time(0), time(23, 59, 59, 999999), [True, True, True, True, False, True, False], '<PeriodicTimeRange 00:00 23:59 [True, True, True, True, False, True, False]>', 'from 00:00 to 23:59 on sun, mon, tue, wed, fri'),
                             (time(0), time(23, 59, 59, 999999), [True, True, True, True, False, True, True], '<PeriodicTimeRange 00:00 23:59 [True, True, True, True, False, True, True]>', 'from 00:00 to 23:59 on sun, mon, tue, wed, fri, sat'),
                             (time(0), time(23, 59, 59, 999999), [True, True, True, True, True, False, False], '<PeriodicTimeRange 00:00 23:59 [True, True, True, True, True, False, False]>', 'from 00:00 to 23:59 on sun, mon, tue, wed, thu'),
                             (time(0), time(23, 59, 59, 999999), [True, True, True, True, True, False, True], '<PeriodicTimeRange 00:00 23:59 [True, True, True, True, True, False, True]>', 'from 00:00 to 23:59 on sun, mon, tue, wed, thu, sat'),
                             (time(0), time(23, 59, 59, 999999), [True, True, True, True, True, True, False], '<PeriodicTimeRange 00:00 23:59 [True, True, True, True, True, True, False]>', 'from 00:00 to 23:59 on sun, mon, tue, wed, thu, fri'),
                             (time(0), time(23, 59, 59, 999999), [True, True, True, True, True, True, True], '<PeriodicTimeRange 00:00 23:59 [True, True, True, True, True, True, True]>', 'daily from 00:00 to 23:59'),
                         ])
def test_absolute_time_range(t_start, t_stop, t_weekdays, t_repr, t_str):
    if t_start > t_stop:
        with pytest.raises(RuntimeError):
            t = PeriodicTimeRange(t_start, t_stop, *t_weekdays)

    if not any(t_weekdays):
        with pytest.raises(RuntimeError):
            t = PeriodicTimeRange(t_start, t_stop, *t_weekdays)

    else:
        t = PeriodicTimeRange(t_start, t_stop, *t_weekdays)
        assert t.start == t_start
        assert t.stop == t_stop
        assert t.weekdays == t_weekdays
        assert repr(t) == t_repr
        assert str(t) == t_str
